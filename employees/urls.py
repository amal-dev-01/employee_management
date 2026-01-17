from django.urls import path
from employees.views import employee_create, employee_list, employee_update, employee_delete

urlpatterns = [

    path("", employee_list, name="employee_list"),
    path("create/<int:form_id>/", employee_create, name="employee_create"),
    path("update/<int:pk>/", employee_update, name="employee_update"),
    path("<int:pk>/delete/", employee_delete, name="employee_delete"),

]
