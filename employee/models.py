from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=12, blank=True, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    emp_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    issue_date = models.DateField()
    
    def __str__(self):
        return self.name
    


