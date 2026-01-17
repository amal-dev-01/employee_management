from django.core.validators import validate_email
from datetime import datetime
from rest_framework import serializers
from rest_framework import serializers
from form_builder.models import FormField, CustomForm
from form_builder.models import CustomForm, FormField
from employees.models import Employee

    

class EmployeeListSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()
    form_name = serializers.CharField(source='form.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'form_name', 'values']

    def get_values(self, obj):
        result = {}
        for ev in obj.values.all():
            field = ev.field
            if 'password' in field.field_type.lower():
                result[field.label] = '********'
            else:
                result[field.label] = ev.value
        return result



class EmployeeFieldInputSerializer(serializers.Serializer):
    field_id = serializers.IntegerField()
    value = serializers.CharField(allow_blank=True)



class EmployeeCreateUpdateSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()
    fields = EmployeeFieldInputSerializer(many=True)

    def validate(self, data):
        form_id = data.get("form_id")
        fields = data.get("fields", [])

        # Check form exists
        try:
            form = CustomForm.objects.get(id=form_id)
        except CustomForm.DoesNotExist:
            raise serializers.ValidationError({"form_id": "Form does not exist"})

        for f in fields:
            try:
                field = FormField.objects.get(id=f["field_id"], form=form)
            except FormField.DoesNotExist:
                raise serializers.ValidationError({"fields": f"Field id {f['field_id']} not found in form"})

            value = f.get("value", "")

            # Dynamic type validation
            if field.field_type == "number":
                if value and not str(value).isdigit():
                    raise serializers.ValidationError({f"field_{field.id}": f"{field.label} must be a number"})
            elif field.field_type == "date":
                if value:
                    try:
                        datetime.strptime(value, "%Y-%m-%d") 
                    except ValueError:
                        raise serializers.ValidationError({f"field_{field.id}": f"{field.label} must be a valid date (YYYY-MM-DD)"})
            elif field.field_type == "email":
                if value:
                    try:
                        validate_email(value)
                    except Exception:
                        raise serializers.ValidationError({f"field_{field.id}": f"{field.label} must be a valid email address"})
        return data
