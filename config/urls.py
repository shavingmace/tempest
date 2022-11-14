"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 주 url 핸들링 파일. 

from django.contrib import admin
from django.urls import path, include
from tempest import views as tp_views

urlpatterns = [
    path('', tp_views.index, name='index'),
    path('admin/', admin.site.urls),
    
    #여기 있는 include() 구문을 사용해 config 외의 하위 앱의 urls.py 파일을 묶어둔다. 
    path('tempest/', include('tempest.urls'), name='tempest'), 
    path('common/', include('common.urls'))
]
