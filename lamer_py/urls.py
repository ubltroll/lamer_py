"""lamer_py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from milicien import views
from django.conf import settings
from django.conf.urls.static import static
import os


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login1),
    path('FAQ/', views.index), #TODO
    path('LogMeIn/', views.LogMeIn),
    path('SignMeUp/', views.SignMeUp),
    path('register/', views.register),
    path('<int:invitorID>', views.index),
    path('register/<int:invitorID>', views.register),
    path('register/CheckName', views.CheckName),
    path('register/CheckName2', views.CheckName2),
    path('register/CheckEmail', views.CheckEmail),
    path('register/CheckPhone', views.CheckPhone),
    path('user/checkin', views.checkin),
    path('user/assist', views.assist),
    path('user/getship', views.getship),
    path('nb123/', views.Setpsd1), #改密码
    path('nb123/2', views.Setpsd2), #改密码
  #  path('register/CheckSMS', views.CheckSMS),
    path('test', views.test),
    path('sys/seal/<int:sealnum>', views.seal), #海豹计划
    path('register/null', views.SentSMS),  #伪装
    path('home/', views.home),
    path('findmypwd/', views.findpsd),
    path('learn/', views.learn),
    path('logout/', views.logout_view),
    path('update/<int:code>', views.update),
    path('act/<int:code>', views.act),
    path('presell/', views.presell),
    path('notice', views.notice),
]
#+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
