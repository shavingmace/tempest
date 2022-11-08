from django.urls import path
from . import views

app_name = 'tempest'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('jsontest/', views.jsontest, name='jsontest'),
]
