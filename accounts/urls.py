from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', views.EmployeeRegistration.as_view(),name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('change_password/',views.ChangePasswordView.as_view(), name='change_password'),
]

