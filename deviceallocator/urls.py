"""
URL configuration for deviceallocator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from services.views import *
from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name="index"),
    path('dashboard/',dashboard, name="dashboard"),
    path('login/',log_in, name="login"),
    path('register/',register, name="register"),
    path('logout/',log_out, name="logout"),
    path('adddevice/',add_device, name="adddevice"),
    path('removedevice/',remove_device, name="removedevice"),
    path('devices/',devices, name="devices"),
    path('devicelog/<device>',device_log, name="devicelog"),
    path('deviceassign/<device_id>',device_assign, name="deviceassign"),
    path('devicereturn/<device_id>',device_return, name="devicereturn"),
    path('addemployee/',add_employee, name="addemployee"),
    path('employee/',employee, name="employee"),
    path('employeelog/<employee>',employee_log, name="employeelog"),
    path('removeemployee/',remove_employee, name="removeemployee"),
    path('editdevice/<device_id>',edit_device_condition, name="editdevice")    
]
