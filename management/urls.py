from django.urls import path
from . import views
urlpatterns = [
    path('forms/',views.EmployeeFormView.as_view(),name='forms'),
    path('profile/',views.UpdateEmployeeFormDataAPIView.as_view(),
         name='get_employee_profile'),
    path('profile/<int:profile_id>/',views.UpdateEmployeeFormDataAPIView.as_view(),
         name='update_employee_profile'),
]
