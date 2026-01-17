from django import forms
from form_builder.models import CustomForm, FormField


class CustomFormForm(forms.ModelForm):
    class Meta:
        model = CustomForm
        fields = ['name', 'description']


class FormFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ['label', 'field_type', 'order']
        widgets = {'order': forms.HiddenInput()}
