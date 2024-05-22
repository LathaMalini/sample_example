# shifts/forms.py
from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position']

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift_type']


from django import forms
from .models import EmployeeShift, Employee, Shift

class BulkShiftAssignForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.CheckboxSelectMultiple)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all())
    from_date = forms.DateField(widget=forms.SelectDateWidget)
    to_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = EmployeeShift
        fields = ['employees', 'shift', 'from_date', 'to_date']

