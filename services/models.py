from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.

#Each User object is a Company with an account

class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)
    department = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    
class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    current_holder = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(unique=True, max_length=300)
    device_type = models.CharField(max_length=200)
    condition =models.TextField()
    specification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        return self.name


class Allocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_condition = models.TextField()
    returned_condition = models.TextField(default=None, null=True)
    assigned_at = models.DateTimeField(null=False)
    returned_at = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.id) 
      
    def clean(self):
        super().clean()

        # Check if both assigned_at and returned_at have values
        if self.assigned_at and self.returned_at:
            # Ensure returned_at is greater than assigned_at
            if self.returned_at <= self.assigned_at:
                raise ValidationError("Returned time must be greater than assigned time.")
