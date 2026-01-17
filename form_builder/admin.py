from django.contrib import admin
from form_builder.models import CustomForm, FormField

@admin.register(CustomForm)
class CustomFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'label', 'field_type')
