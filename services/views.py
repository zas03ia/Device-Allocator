from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dasboard.html')
    return render(request, 'index.html')
        

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform form validation
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('login')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login successful
            login(request, user)
            return redirect('/')
        else:
            # Login failed
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        company = request.POST.get('companyname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform form validation
        if not company or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('signup')

        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists() or User.objects.filter(username=company).exists():
            messages.error(request, 'An account already exists with this email.')
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=company, email=email, password=password)
        user.save()

        messages.success(request, 'Account created successfully. Please log in!')
        return redirect('/')

    return render(request, 'signup.html')

def logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def adddevice(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        device_type = request.POST.get('device_type')
        condition = request.POST.get('condition')
        specification = request.POST.get('specification')

        # Perform form validation
        if not name or not device_type or not condition or not specification:
            messages.error(request, 'All fields are required.')
            return redirect('adddevice')

        # Check if a device with the given name already exists
        if Device.objects.filter(name=name).exists():
            messages.error(request, 'A device already exists with this name. Use a different name for individual device identification')
            return redirect('adddevice')

        # Create new device instance
        device = Device(name=name, device_type=device_type, condition=condition, specification=specification)
        device.save()

        messages.success(request, 'Device added successfully')
        return redirect('dashboard')

    return render(request, 'adddevice.html')

def addemployee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        position = request.POST.get('position')

        # Perform form validation
        if not name:
            messages.error(request, 'Employee name is required.')
            return redirect('addemployee')

        # Check if an employee with the given name already exists
        if Employee.objects.filter(name=name).exists():
            messages.error(request, 'An employee already exists with this name. Use a different name for individual employee identification')
            return redirect('addemployee')

        # Create new device instance
        employee = Employee(name=name)
        if department:
            employee.department=department    
        if position:
            employee.position=position
        employee.save()

        messages.success(request, 'Employee added successfully')
        return redirect('dashboard')

    return render(request, 'addemployee.html')

def devices(request):
    pass

def devicelog(request):
    pass

def deviceassign(request):
    pass

def devicereturn(request):
    pass

def employee(request):
    pass

def employeelog(request):
    pass
