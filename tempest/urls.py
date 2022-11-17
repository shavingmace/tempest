from django.urls import path
from . import views

app_name = 'tempest'

urlpatterns = [
    path('record_bak/', views.record_form, name='record_form_bak'),
    path('record/', views.record_form, name='record_form'),
    path('record/post/', views.record_post, name='record_post'),
    path('record/recorded/', views.recorded, name='recorded'),
    path('test/', views.test, name='test'), 
    path('jsontest/', views.jsontest, name='jsontest'),
    path('showpastwthr/<str:date>', views.show_past_wthr, name='show_wthr'),
    path('recordcntwthr/', views.record_current_wthr, name='record_current_wthr' ) # 임의적으로 데이터베이스에 현재 시간의 시간 기록 
]
