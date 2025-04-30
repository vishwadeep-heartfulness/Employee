from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    phonenumber= models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    dateofjoining = models.DateField()
    experience = models.IntegerField()
    


class Project(models.Model):
    name = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()

    
