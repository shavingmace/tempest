from django.urls import path
from . import views
from jsonrpc import jsonrpc_site

app_name = 'tempest'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('json/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
]
