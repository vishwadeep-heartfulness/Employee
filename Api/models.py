from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    phonenumber= models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    dateofjoining = models.DateField()
    experience = models.IntegerField()
    

    def __str__(self):
        return self.name

class Project(models.Model):
    projectname = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()

    def __str__(self):
        return self.projectname
