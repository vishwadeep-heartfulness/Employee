# serializers.py
from rest_framework import serializers
from .models import User
from .models import Employee, Project
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # ONLY these fields
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
     user = User.objects.create_user(**validated_data)
     return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token  

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'dob','phonenumber', 'domain', 'company','dateofjoining', 'experience']

class ProjectSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'employee', 'employee_name', 'status', 'startdate', 'enddate']
