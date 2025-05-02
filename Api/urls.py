from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, ProjectViewSet, CustomTokenObtainPairView, RegisterView

router = DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('projects', ProjectViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
