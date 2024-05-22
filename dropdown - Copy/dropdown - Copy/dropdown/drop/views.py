# shifts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ShiftForm

def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'shift_list.html', {'shifts': shifts})

def shift_create(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shift_list')
    return redirect('shift_list')

def shift_update(request, shift_id):
    shift = get_object_or_404(Shift, shift_id=shift_id)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('shift_list')
    return redirect('shift_list')

def shift_delete(request, shift_id):
    shift = get_object_or_404(Shift, shift_id=shift_id)
    if request.method == 'POST':
        shift.delete()
        return redirect('shift_list')
    return redirect('shift_list')



# shifts/views.py
from django.shortcuts import render, redirect
from .models import EmployeeShift
from .forms import BulkShiftAssignForm
def bulk_shift_assign(request):
    if request.method == 'POST':
        form = BulkShiftAssignForm(request.POST)
        if form.is_valid():
            employees = request.POST.getlist('employees')
            shift = form.cleaned_data['shift']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            
            for employee_id in employees:
                employee = get_object_or_404(Employee, pk=employee_id)
                EmployeeShift.objects.create(employee=employee, shift=shift, from_date=from_date, to_date=to_date)
            
            return redirect('bulk_shift_assign')
    else:
        form = BulkShiftAssignForm()
    employees = Employee.objects.all()
    return render(request, 'bulk_shift_assign.html', {'form': form, 'employees': employees})



# views.py
from django.shortcuts import render
from .models import EmployeeShift, Employee
from django.db.models import Q
from datetime import datetime, timedelta

def employee_shifts_view(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    else:
        from_date = None
        to_date = None

    employee_shifts = EmployeeShift.objects.select_related('employee', 'shift')

    if from_date and to_date:
        employee_shifts = employee_shifts.filter(
            Q(from_date__lte=to_date) & Q(to_date__gte=from_date)
        )

    employees = Employee.objects.prefetch_related(
        'employeeshift_set__shift'
    ).all()

    date_range = []
    if from_date and to_date:
        current_date = from_date
        while current_date <= to_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)

    # Create a dictionary with employees and their respective shifts
    employees_with_shifts = []
    for employee in employees:
        shifts = employee.employeeshift_set.filter(
            Q(from_date__lte=to_date) & Q(to_date__gte=from_date)
        ) if from_date and to_date else []
        employees_with_shifts.append({'name': employee.name, 'shifts': shifts})

    context = {
        'employee_shifts': employee_shifts,
        'employees': employees_with_shifts,
        'date_range': date_range,
        'from_date': from_date,
        'to_date': to_date,
    }

    return render(request, 'employee_shift.html', context)
  

