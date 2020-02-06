from django.forms import ModelForm
from .models import Employee, Punch
from django import forms

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'address', 'phone','isadmin', 'department','username','email','password')

class PunchForm(ModelForm):
    class Meta:
        model = Punch
        fields = ('punchin', 'punchout', 'date', 'empid')





