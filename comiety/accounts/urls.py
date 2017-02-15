"""comiety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from accounts import views
from django.contrib.auth.views import logout

urlpatterns = [
    # url(r'^login/$', views.login, name = 'login'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^member_info_regist/$', views.member_info_regist, name = 'member_info_regist'),
    url(r'^member_info_regist_edit/$', views.member_info_regist_edit, name = 'member_info_regist_edit'),
    url(r'^member_regist/$', views.member_regist, name = 'member_regist'),
    url(r'^my_profile/$', views.my_profile, name = 'my_profile'),
    # logout auth_view의 로그아웃 사용할지 아니면 올어스 로그아웃 사용할지
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': 'dongzip:index'}),
]