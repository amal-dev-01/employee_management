import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from form_builder.models import CustomForm, FormField
from employees.models import Employee, EmployeeFieldValue



# ---------------- Employee List ----------------

@login_required
def employee_list(request):
    search_text = request.GET.get("q", "").strip().lower()
    search_field = request.GET.get("field", "")

    forms = CustomForm.objects.all()

    labels = []
    seen = set()
    for f in FormField.objects.all():
        if f.label not in seen:
            seen.add(f.label)
            labels.append(f.label)

    employees = Employee.objects.prefetch_related(
        "values",
        "values__field"
    )

    rows = []

    for emp in employees:
        value_map = {}

        for v in emp.values.all():
            field_type = v.field.field_type.lower()

            if "password" in field_type:
                value_map[v.field.label] = "********"
            else:
                value_map[v.field.label] = v.value


        if search_text and search_field:
            field_value = value_map.get(search_field, "").lower()
            if search_text not in field_value:
                continue

        rows.append({
            "id": emp.id,
            "values": [value_map.get(label, "") for label in labels]
        })

    context = {
        "labels": labels,
        "rows": rows,
        "forms": forms,

        "search_text": search_text,
        "search_field": search_field,
    }
    return render(request, "employee_list.html", context)




# ---------------- Employee Create ----------------
@login_required
def employee_create(request, form_id):
    form = get_object_or_404(CustomForm, id=form_id)
    fields = form.fields.all()

    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        with transaction.atomic():
            employee = Employee.objects.create(form=form)
            for field in fields:
                value = data.get(f"field_{field.id}", "")
                if field.field_type == "number" and value and not str(value).isdigit():
                    return JsonResponse({"status": "error", "message": f"{field.label} must be a number"}, status=400)
                EmployeeFieldValue.objects.create(employee=employee, field=field, value=value)
        return JsonResponse({"status": "success", "redirect_url":reverse('employee_list')})

    return render(request, "employee_form.html", {"form": form, "fields": fields, "values": {}, "is_update": False})




# ---------------- Employee Update ----------------
@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    form = employee.form
    fields = form.fields.all()
    values = {f"field_{ev.field.id}": ev.value for ev in employee.values.all()}

    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        with transaction.atomic():
            for field in fields:
                value = data.get(f"field_{field.id}", "")
                if field.field_type == "number" and value and not str(value).isdigit():
                    return JsonResponse({"status": "error", "message": f"{field.label} must be a number"}, status=400)
                EmployeeFieldValue.objects.update_or_create(employee=employee, field=field, defaults={"value": value})
        return JsonResponse({"status": "success", "redirect_url": reverse('employee_list')})

    return render(request, "employee_form.html", {"form": form, "fields": fields, "values": values, "is_update": True, "employee": employee})


# ---------------- Employee Delete ----------------
@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")
    return render(request, "employee_confirm_delete.html", {"employee": employee})




