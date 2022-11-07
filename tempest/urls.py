from django.urls import path

from . import views

app_name = 'tempest'

urlpatterns = [
    path('', views.index, name='index')
]
