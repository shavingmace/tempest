from django.urls import path
from . import views

app_name = 'tempest'

urlpatterns = [
    path('', views.index, name='index'),    
    path('second/', views.second, name='second'),
    path('test/', views.test, name='test'),
    path('jsontest/', views.jsontest, name='jsontest'),
    path('showpastwthr/<str:date>', views.show_past_wthr, name='show_wthr'),
    path('recordcntwthr/', views.record_current_wthr, name='record_current_wthr' )
]
