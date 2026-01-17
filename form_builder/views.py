from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import modelformset_factory
from form_builder.models import CustomForm, FormField
from form_builder.forms import CustomFormForm, FormFieldForm


# ---------------- Form List ----------------

@login_required
def form_list(request):
    forms = CustomForm.objects.all()
    return render(request, 'form_list.html', {'forms': forms})



# ---------------- Form Create ----------------
@login_required
def form_create(request):
    FieldFormSet = modelformset_factory(FormField, form=FormFieldForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = CustomFormForm(request.POST)
        formset = FieldFormSet(request.POST, queryset=FormField.objects.none())

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    custom_form = form.save()
                    for f in formset:
                        if f.cleaned_data.get('DELETE'):
                            continue
                        field = f.save(commit=False)
                        field.form = custom_form
                        field.save()
                    messages.success(request, "Form created successfully!")
                    return redirect('form_list') 
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Please check all fields for errors.")
    else:
        form = CustomFormForm()
        formset = FieldFormSet(queryset=FormField.objects.none())

    return render(request, 'form_create_formset.html', {
        'form': form,
        'formset': formset
    })



# ---------------- Form Update ----------------
@login_required
def form_update(request, form_id):
    custom_form = get_object_or_404(CustomForm, id=form_id)
    FieldFormSet = modelformset_factory(FormField, form=FormFieldForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = CustomFormForm(request.POST, instance=custom_form)
        formset = FieldFormSet(request.POST, queryset=custom_form.fields.all())

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    for f in formset:
                        if f.cleaned_data.get('DELETE'):
                            if f.instance.pk:
                                f.instance.delete()
                            continue
                        field = f.save(commit=False)
                        field.form = custom_form
                        field.save()
                    messages.success(request, "Form updated successfully!")
                    return redirect('form_list') 
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = CustomFormForm(instance=custom_form)
        formset = FieldFormSet(queryset=custom_form.fields.all())

    return render(request, 'form_update_formset.html', {
        'form': form,
        'formset': formset,
        'custom_form': custom_form
    })
