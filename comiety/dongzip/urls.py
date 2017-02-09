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
from django.conf.urls import url
from django.contrib import admin
from dongzip import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^member_info_regist/$', views.member_info_regist, name = 'member_info_regist' ),
    url(r'^school_list/$', views.school_list, name = 'school_list'),
    url(r'^school_list/(?P<id>\d+)/$', views.society_list, name = 'society_list'),
    url(r'^society_search/$', views.society_search, name = 'society_search'),
    url(r'^society_regist/$', views.society_regist, name = 'society_regist'),
    url(r'^society_detail/(?P<id>\d+)/$', views.society_detail, name = 'society_detail'),
    url(r'^login/$', accounts_views.login, name = 'login'),
    url(r'^ajax_counter/$', views.ajax_counter, name = 'ajax_counter'),

]
