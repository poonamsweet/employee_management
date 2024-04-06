"""
URL configuration for employee_management project.

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
from employee.views import LoginView, AddEmployee, ViewAllEmployee, UpdateEmployee, DeleteEmployee, GenerateSaleryReport, get_json_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView, name="login"),
    path('add_employee/', AddEmployee, name="add_employee"),
    path('view_all_employee/', ViewAllEmployee, name="view_all_employee"),
    path('update_employee/<int:id>/', UpdateEmployee, name="update_employee"),
    path('delete_employee/<int:id>/', DeleteEmployee, name="delete_employee"),
    path('monthly_salary_report/', GenerateSaleryReport, name="monthly_salary_report"),
    path("get_data/", get_json_data, name="get_data")
]
