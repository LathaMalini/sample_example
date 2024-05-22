# shifts/admin.py
from django.contrib import admin
from .models import *

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_id', 'shift_type')
    search_fields = ('shift_type',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'position')

@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift', 'from_date', 'to_date')
    list_filter = ('employee', 'shift')