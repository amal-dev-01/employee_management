from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api_views import LoginAPIView, LogoutAPIView,RegisterAPIView


urlpatterns = [
    
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

]