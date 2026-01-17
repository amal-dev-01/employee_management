from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from employees.models import Employee, EmployeeFieldValue
from form_builder.models import FormField, CustomForm
from employees.serializers import EmployeeCreateUpdateSerializer

# ---------------- Employee List API----------------

class EmployeeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        search_text = request.GET.get('q', '').lower()
        search_field = request.GET.get('field', '')
        employees = Employee.objects.prefetch_related('values', 'values__field').all()
        result = []

        for emp in employees:
            fields_data = []

            for ev in emp.values.all():
                field = ev.field
                value = ev.value

                if 'password' in field.field_type.lower():
                    value = '********'

                fields_data.append({
                    "field_id": field.id,
                    "label": field.label,
                    "field_type": field.field_type,
                    "value": value
                })

            if search_text and search_field:
                search_field_lower = search_field.lower()
                matched_field = next(
                    (f for f in fields_data if f["label"].lower() == search_field_lower), 
                    None
                )
                field_value = str(matched_field["value"]).lower() if matched_field else ""
                if search_text not in field_value:
                    continue

            result.append({
                "id": emp.id,
                "form_id": emp.form.id,
                "form_name": emp.form.name,
                "fields": fields_data
            })

        return Response(result, status=status.HTTP_200_OK)


# ---------------- Employee Create API----------------

class EmployeeCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = EmployeeCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        form_id = serializer.validated_data['form_id']
        fields_data = serializer.validated_data['fields']
        form = CustomForm.objects.get(id=form_id)

        try:
            with transaction.atomic():
                employee = Employee.objects.create(form=form)
                for f in fields_data:
                    field = FormField.objects.get(id=f['field_id'])
                    EmployeeFieldValue.objects.create(employee=employee, field=field, value=f['value'])

            return Response({
                "employee_id": employee.id,
                "form_id": form.id,
                "form_name": form.name,
                "fields": [
                    {
                        "field_id": f.field.id,
                        "label": f.field.label,
                        "type": f.field.field_type,
                        "value": f.value
                    } for f in employee.values.all()
                ]
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": "error", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Employee Update API----------------

class EmployeeUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def put(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"status": "error", "error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        form_id = serializer.validated_data['form_id']
        fields_data = serializer.validated_data['fields']

        if employee.form.id != form_id:
            return Response({"status": "error", "error": "Form does not match employee"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for f in fields_data:
                    field = FormField.objects.get(id=f['field_id'])
                    EmployeeFieldValue.objects.update_or_create(
                        employee=employee,
                        field=field,
                        defaults={"value": f['value']}
                    )

            return Response({
                "status": "success",
                "employee_id": employee.id,
                "form_id": employee.form.id,
                "form_name": employee.form.id,
                "fields": [
                    {
                        "field_id": ev.field.id,
                        "label": ev.field.label,
                        "type": ev.field.field_type,
                        "value": "********" if "password" in ev.field.field_type.lower() else ev.value
                    } for ev in employee.values.all()
                ]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Employee Delete API----------------

class EmployeeDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_200_OK)
