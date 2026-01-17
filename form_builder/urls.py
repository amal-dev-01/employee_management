from django.urls import path
from form_builder.views import form_list, form_create,form_update

urlpatterns = [

    path('', form_list, name='form_list'),
    path('create/', form_create, name='form_create'),
    path('<int:form_id>/edit/', form_update, name='form_edit'),

]
