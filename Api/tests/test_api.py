import pytest
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import User, Employee, Project
from faker import Faker
from django.contrib.contenttypes.models import ContentType

fake = Faker()

@pytest.fixture
def manager_group(db):
    group, _ = Group.objects.get_or_create(name='Manager')
    # Assign all permissions related to Employee and Project to the manager group
    for model in [Employee, Project]:
        content_type = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(content_type=content_type)
        group.permissions.set(list(perms) + list(group.permissions.all()))
    return group

@pytest.fixture
def employee_group(db):
    group, _ = Group.objects.get_or_create(name='Employee')
    # Give only read permissions
    read_perms = Permission.objects.filter(codename__startswith='view')
    group.permissions.set(read_perms)
    return group

@pytest.fixture
def create_user(db):
    def make_user(username, group=None):
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password="TestPass123"
        )
        if group:
            user.groups.add(group)
        return user
    return make_user

@pytest.fixture
def get_token():
    def login(username, password):
        client = APIClient()
        url = reverse('token_obtain_pair')
        response = client.post(url, {'username': username, 'password': password}, format='json')
        return response.data['access']
    return login


@pytest.mark.django_db
def test_manager_can_create_employee(manager_group, create_user, get_token):
    # Create a user with Manager group
    user = create_user('manager_user', manager_group)
    token = get_token('manager_user', 'TestPass123')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = reverse('employee-list')
    data = {
        "name": fake.name(),
        "email": fake.email(),
        "dob": fake.date_of_birth(minimum_age=25, maximum_age=40),
        "phonenumber": fake.phone_number(),
        "domain": fake.job(),
        "company": fake.company(),
        "dateofjoining": fake.date_this_decade(),
        "experience": fake.random_int(min=1, max=15)
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201  # Created
    


@pytest.mark.django_db
def test_employee_cannot_create_project(employee_group, create_user, get_token):
    # Create a user with Employee group
    user = create_user('employee_user', employee_group)
    token = get_token('employee_user', 'TestPass123')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = reverse('project-list')
    data = {
        "name": fake.bs(),
        "employee": None,  # Required, so this should return 400 anyway
        "status": "In Progress",
        "startdate": fake.date_this_year(),
        "enddate": fake.date_this_year()
    }

    response = client.post(url, data, format='json')
    assert response.status_code in [403, 400]  # Permission Denied or Bad Request


@pytest.mark.django_db
def test_manager_can_create_project(manager_group, create_user, get_token):
    # Step 1: Create manager user and get token
    user = create_user('manager_project_user', manager_group)
    token = get_token('manager_project_user', 'TestPass123')

    # Step 2: Create an employee to assign the project to
    employee = Employee.objects.create(
        name=fake.name(),
        email=fake.unique.email(),
        dob=fake.date_of_birth(minimum_age=25, maximum_age=40),
        phonenumber=fake.phone_number(),
        domain=fake.job(),
        company=fake.company(),
        dateofjoining=fake.date_this_decade(),
        experience=fake.random_int(min=1, max=15)
    )

    # Step 3: Use token to send authorized POST request
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = reverse('project-list')
    data = {
        "name": fake.bs(),
        "employee": employee.id,
        "status": "In Progress",
        "startdate": fake.date_this_year(),
        "enddate": fake.date_this_year()
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201  # Created


@pytest.mark.django_db
def test_anonymous_user_cannot_access_api():
    client = APIClient()
    response = client.get(reverse('employee-list'))
    assert response.status_code == 401  # Unauthorized
