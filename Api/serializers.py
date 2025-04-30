# serializers.py
from rest_framework import serializers
from .models import User
from .models import Employee, Project
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # ONLY these fields
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'dob','phonenumber', 'domain', 'company','dateofjoining', 'experience']

class ProjectSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'projectname', 'employee', 'employee_name', 'status', 'startdate', 'enddate']
