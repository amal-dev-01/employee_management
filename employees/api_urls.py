from django.urls import path
from employees.api_views import EmployeeCreateAPIView, EmployeeDeleteAPIView,EmployeeListAPIView, EmployeeUpdateAPIView

urlpatterns = [

    path('', EmployeeListAPIView.as_view(), name='employee_list_api'),
    path('create/', EmployeeCreateAPIView.as_view(), name='employee_create_api'),
    path('<int:pk>/update/', EmployeeUpdateAPIView.as_view(), name='employee_update_api'),
    path('<int:pk>/delete/', EmployeeDeleteAPIView.as_view(), name='employee_delete_api'),

]
