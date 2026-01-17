from django.contrib import admin
from employees.models import Employee, EmployeeFieldValue

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'created_at')


@admin.register(EmployeeFieldValue)
class EmployeeFieldValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee')
