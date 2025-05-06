from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class EmployeeProjectTestCase(APITestCase):
    def setUp(self):
        # Create or get the Manager group
        manager_group, _ = Group.objects.get_or_create(name='Manager')

        # Assign permissions to the Manager group
        permissions = Permission.objects.filter(
            codename__in=[
                'add_employee', 'view_employee', 'change_employee', 'delete_employee',
                'add_project', 'view_project', 'change_project', 'delete_project'
            ]
        )
        manager_group.permissions.set(permissions)

        # Create a user and add to Manager group
        self.user = User.objects.create_user(username='Rahim', email='rahim@example.com', password='Rahim123')
        self.user.groups.add(manager_group)

        # Authenticate as this user
        self.client.force_authenticate(user=self.user)

    def test_create_employee(self):
        employee_data = {
            "name": "Mithra",
            "email": "mithra@example.com",
            "dob": "1995-05-01",
            "phonenumber": "9876543210",
            "domain": "Frontend",
            "company": "Tech Ltd",
            "dateofjoining": "2022-02-01",
            "experience": 3
        }
        response = self.client.post("/api/employees/", employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_project(self):
        # First, create an employee to associate with the project
        employee_response = self.client.post("/api/employees/", {
            "name": "Mithra",
            "email": "mithra@example.com",
            "dob": "1995-05-01",
            "phonenumber": "9876543210",
            "domain": "Frontend",
            "company": "Tech Ltd",
            "dateofjoining": "2022-02-01",
            "experience": 3
        }, format='json')
        self.assertEqual(employee_response.status_code, status.HTTP_201_CREATED)

        employee_id = employee_response.data["id"]

        # Then, create the project
        project_data = {
            "name": "Website Redesign",
            "employee": employee_id,
            "status": "Ongoing",
            "startdate": "2024-01-01",
            "enddate": "2024-06-01"
        }
        project_response = self.client.post("/api/projects/", project_data, format='json')
        self.assertEqual(project_response.status_code, status.HTTP_201_CREATED)
