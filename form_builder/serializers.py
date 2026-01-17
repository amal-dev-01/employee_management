from rest_framework import serializers
from form_builder.models import CustomForm, FormField


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_type', 'order']


class CustomFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = CustomForm
        fields = ['id', 'name', 'description', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        custom_form = CustomForm.objects.create(**validated_data)

        for i, field_data in enumerate(fields_data):
            field_order = field_data.pop('order', i)
            FormField.objects.create(
                form=custom_form,
                order=field_order,
                **field_data
            )

        return custom_form

    # def update(self, instance, validated_data):
    #     fields_data = validated_data.pop('fields', [])
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()

    #     # Track field IDs sent by client
    #     new_ids = [f.get('id') for f in fields_data if f.get('id')]
    #     # Delete fields that were removed
    #     instance.fields.exclude(id__in=new_ids).delete()

    #     for i, field_data in enumerate(fields_data):
    #         field_id = field_data.get('id', None)
    #         field_order = field_data.pop('order', i)  # Use passed order or default i

    #         if field_id:
    #             # Update existing field
    #             field = FormField.objects.get(id=field_id, form=instance)
    #             field.label = field_data.get('label', field.label)
    #             field.field_type = field_data.get('field_type', field.field_type)
    #             field.order = field_order
    #             field.save()
    #         else:
    #             # Create new field
    #             FormField.objects.create(
    #                 form=instance,
    #                 order=field_order,
    #                 **field_data
    #             )

    #     return instance
