from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.http import request


class Registration(UserCreationForm): #for registration of a Company. Each user is a Company that has an account.
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Login(AuthenticationForm):
    pass

class addDevice(forms.ModelForm): # form for adding a new device
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'condition', 'specification']
        
        
class addEmployee(forms.ModelForm): # form for adding a new employee
    class Meta:
        model = Employee
        fields = ['name', 'department', 'position']
        
        
class allocate(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs): 
        super(allocate, self).__init__(*args, **kwargs)
        
        # Customize queryset for employee_id field for specific user
        if user:
            self.fields['employee_id'].queryset = Employee.objects.filter(user=user)

    class Meta:
        model = Allocation
        fields = ['employee_id', 'assigned_condition', 'assigned_at']
        widgets = {
            'assigned_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class return_device(forms.ModelForm): # form that stores information on device return
    class Meta:
        model = Allocation
        fields = ['returned_condition','returned_at']
        widgets = {
            'returned_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class edit_device(forms.ModelForm): # form to update device condition
    class Meta:
        model = Device
        fields = ['condition']