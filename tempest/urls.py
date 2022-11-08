from django.urls import path
from . import views

app_name = 'tempest'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('jsontest/', views.jsontest, name='jsontest'),
    path('showpastwthr/<str:date>', views.show_past_wthr, name='show_wthr'),
    path('showcurrentwthr/', views.show_current_wthr, name='show_current_wthr' )
]
