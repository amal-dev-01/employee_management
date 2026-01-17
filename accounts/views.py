from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from accounts.forms import (
    RegisterForm, LoginForm,
    ProfileUpdateForm, ChangePasswordForm
)
from employees.models import Employee
from form_builder.models import CustomForm


# ---------------- Register ----------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                messages.success(request, "Account created successfully. Please login.")
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                login(request, user)
                return redirect('home')
            
            except Exception:
                messages.error(request, "Something went wrong. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



# ---------------- Login ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is None:
            messages.error(request, "Invalid username or password")
        elif not user.is_active:
            messages.error(request, "Your account is inactive")
        else:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')

    return render(request, 'login.html', {'form': form})


# ---------------- Profile ----------------
@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "Profile updated successfully")
                return redirect('home')
            except Exception:
                messages.error(request, "Unable to update profile")
        else:
            messages.error(request, "Please fix the errors below")
    return render(request, 'profile.html', {'form': form})


# ---------------- CHANGE PASSWORD ----------------
@login_required
def change_password_view(request):
    form = ChangePasswordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if not request.user.check_password(form.cleaned_data['old_password']):
            messages.error(request, "Old password is incorrect")
        else:
            try:
                with transaction.atomic():
                    request.user.set_password(form.cleaned_data['new_password'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)

                messages.success(request, "Password changed successfully")
                return redirect('home')

            except Exception:
                messages.error(request, "Password update failed")

    return render(request, 'change_password.html', {'form': form})


# ---------------- Logout ----------------
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect('login')


# ---------------- Home ----------------
@login_required
def home(request):
    total_employees_count = Employee.objects.count()
    total_form_count = CustomForm.objects.count()
    recent_forms = CustomForm.objects.order_by('-created_at')[:5]

    return render(request, 'home.html', {
        'total_employees_count': total_employees_count,
        'total_form_count': total_form_count,
        'recent_forms': recent_forms,
    })

