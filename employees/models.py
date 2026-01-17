from django.db import models
from form_builder.models import CustomForm, FormField

class Employee(models.Model):
    form = models.ForeignKey(CustomForm, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee {self.id}"


class EmployeeFieldValue(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="values"
    )
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.field.label}: {self.value}"
