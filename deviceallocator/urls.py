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
    path('',dashboard, name="dashboard"),
    path('login/',login, name="login"),
    path('register/',register, name="register"),
    path('logout/',logout, name="logout"),
    path('adddevice/',adddevice, name="adddevice"),
    path('devices/',devices, name="devices"),
    path('devicelog/',devicelog, name="devicelog"),
    path('deviceassign/',deviceassign, name="deviceassign"),
    path('devicereturn/',devicereturn, name="devicereturn"),
    path('addemployee/',addemployee, name="addemployee"),
    path('employee/',employee, name="employee"),
    path('employeelog/',employeelog, name="employeelog"),
]
