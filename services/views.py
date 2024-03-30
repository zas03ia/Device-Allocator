from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *



#______________________# for api documentation

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import viewsets

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
class AllocationViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer

class DeviceList(APIView):
    def get(self, request):
        queryset = Device.objects.all()
        serializer = DeviceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeList(APIView):
    def get(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AllocationList(APIView):
    def get(self, request):
        queryset = Allocation.objects.all()
        serializer = AllocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AllocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#______________________#



def index(request):
    if request.user.is_authenticated: # check for authentication
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'dashboard.html') 
        

def log_in(request):
    if request.method == 'POST':
        form = Login(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = Login()
    return render(request, 'form.html', {'form': form, 'title': 'Login', 'val': "Login"})

def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = Registration()
    return render(request, 'form.html', {'form': form, 'title': 'Register', 'val': "Register"})

@login_required
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

@login_required
def add_device(request): # add new device 
    if request.method == 'POST':
        form = addDevice(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('dashboard')
    else:
        form = addDevice()
    
    return render(request, 'form.html', {'form': form, 'title': 'New Device', 'val': "Add"})

@login_required
def add_employee(request): #add new employee
    if request.method == 'POST':
        form = addEmployee(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user # Allocating to Company
            instance.save()
            return redirect('dashboard')  
    else:
        form = addEmployee()
    
    return render(request, 'form.html', {'form': form, 'title': 'New Employee', 'val': "Add"})

@login_required
def devices(request): # show existing devices specific to company
    devices = Device.objects.filter(user=request.user.id)
    return render(request, 'devices.html', {'devices':devices})

@login_required
def device_log(request, device): # show selected device log
    log = Allocation.objects.filter(device_id=device, user=request.user.id)
    return render(request, 'device_log.html', {'log':log, 'id': device})

@login_required
def device_assign(request, device_id): # assign a device
    if request.method=="POST":
        # feych device to be allocated
        device = Device.objects.get(id=request.session.get('device'), user=request.user.id) 
        
        #check for availability
        if device.assigned:
            return redirect('devices')
        form = allocate(request.POST, user=request.user.id)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.device_id = device
            allocation.user = request.user
            allocation.save()
            device.assigned = True #change device status
            device.current_holder = allocation.employee_id #update device holder
            device.save()
            del request.session['device']
            return redirect('devices')
        return redirect(f'/deviceassign/{device.id}')
    else:
        request.session['device']=device_id
        device = Device.objects.get(id=request.session.get('device'), user=request.user.id)
        if device.assigned:
            return redirect('devices')
        form = allocate(user=request.user.id, initial={'assigned_condition':device.condition})
        return render(request, 'form.html', {'form': form, 'title': f'Assign device {device.name}', 'val': "Assign"})

@login_required
def device_return(request, device_id):
    try:
        device = Device.objects.get(id=device_id, user=request.user.id)
        allocation = Allocation.objects.get(device_id=device_id, employee_id=device.current_holder, user=request.user.id)
        instance = get_object_or_404(Allocation, pk=allocation.id)
    except Allocation.DoesNotExist:
        # Handle case where no matching allocation is found
        return redirect('devices')
    instance = get_object_or_404(Allocation, pk= allocation.id)
    if request.method=="POST":
        form = return_device(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            device.assigned = False # update status
            device.current_holder = None # remove device holder
            device.save()
            del request.session['device']
            return redirect('devices') 
    else:
        request.session['device']=device_id
        form = return_device(instance=instance)
        return render(request, 'form.html', {'form': form, 'title': f'Return device {device.name}', 'val': "Return"})

@login_required
def employee(request):
    employees = Employee.objects.filter(user=request.user.id)
    return render(request, 'employees.html', {'employees':employees})

@login_required
def employee_log(request, employee):
    log = Allocation.objects.filter(employee_id=employee, user=request.user.id)
    return render(request, 'employee_log.html', {'log':log, 'id':employee})

@login_required
def remove_employee(request):
    if request.method=="POST":
        employee_id = request.POST.get("employee_id")
        employee= Employee.objects.get(id=employee_id, user=request.user.id)
        if employee:
            employee.delete()
    return redirect('employee')

@login_required
def remove_device(request):
    if request.method=="POST":
        device_id = request.POST.get("device_id")
        device= Device.objects.get(id=device_id, user=request.user.id)
        if device:
            device.delete()
    return redirect('devices')

@login_required
def edit_device_condition(request, device_id):
    device = Device.objects.get(id=device_id, user=request.user.id)
    device = get_object_or_404(Device, pk= device.id)   # accessspecific device object for form implementation 
    if request.method=="POST":
        if device is None:
            return redirect('devices')
        form = edit_device(request.POST, instance=device) # initialise form specific to employee and device
        if form.is_valid():
            form.save()
            return redirect('devices') 
    else:
        if device is None:
            return redirect('devices')
        form = edit_device(instance=device)
        return render(request, 'form.html', {'form': form, 'title': f'Edit device {device.name} condition', 'val': "Save"})