from django.urls import path
from accounts.views import register_view, login_view, logout_view, profile_view, change_password_view, home

urlpatterns = [

    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password_view, name='change_password'),
    path('home/', home, name='home'),

]
