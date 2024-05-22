from django.db import models

# Create your models here.
# shifts/models.py
from django.db import models

class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    shift_type = models.CharField(max_length=100)

    def __str__(self):
        return self.shift_type

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.shift.shift_type} ({self.from_date} to {self.to_date})"
    

    