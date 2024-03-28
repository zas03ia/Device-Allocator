from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)
    department = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    device_type = models.CharField(max_length=200)
    condition = models.CharField(max_length=5000)
    specification = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name


class Allocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_condition = models.CharField(max_length=5000)
    returned_condition = models.CharField(max_length=5000)
    assigned_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name    
    
