from rest_framework import serializers
from django.contrib.auth.models import User
from employee.models import Employee


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = ['username', 'password']


class AddEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'emp_salary', 'designation', 'issue_date']
