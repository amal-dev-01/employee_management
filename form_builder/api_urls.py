from django.urls import path
from form_builder.api_views import CustomFormListCreateAPIView

urlpatterns = [
    path('', CustomFormListCreateAPIView.as_view(), name='api_form_list_create'),
]
