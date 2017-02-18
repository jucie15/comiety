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

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^school_list/$', views.school_list, name = 'school_list'),
    url(r'^school_list/ajax_search/$', views.ajax_search_sch, name = 'ajax_search_sch'),
    url(r'^school_list/(?P<id>\d+)/$', views.school_detail, name = 'school_detail'),
    url(r'^school_list/(?P<id>\d+)/ajax_search/$', views.ajax_search_soc, name = 'ajax_search_soc'),
    url(r'^society_search/(?P<name>[a-z_A-Z]+)/$', views.society_search, name = 'society_search'),
    url(r'^society_search/(?P<name>[a-z_A-Z]+)/ajax_search/$', views.ajax_search_related, name = 'ajax_search_related'),
    url(r'^society_regist/$', views.society_regist, name = 'society_regist'),
    url(r'^society_detail/(?P<id>\d+)/$', views.society_detail, name = 'society_detail'),
    url(r'^society_apply/(?P<id>\d+)/$', views.society_apply, name = 'society_apply'),

    url(r'^society_detail/(?P<id>\d+)/admin/$', views.society_admin, name = 'society_admin'),
    url(r'^society_detail/(?P<id>\d+)/admin/manager_edit/$', views.society_admin_manager_edit, name = 'society_admin_manager_edit'),
    url(r'^society_detail/(?P<id>\d+)/admin/manager_add/$', views.society_admin_manager_add, name = 'society_admin_manager_add'),
    url(r'^society_detail/(?P<id>\d+)/admin/info_edit$', views.society_admin_info_edit, name = 'society_admin_info_edit'),
    url(r'^society_detail/(?P<id>\d+)/admin/member_edit$', views.society_admin_member_edit, name = 'society_admin_member_edit'),
    url(r'^society_detail/(?P<id>\d+)/admin/manager_remove/$', views.society_admin_manager_remove, name = 'society_admin_manager_remove'),
    url(r'^society_detail/(?P<id>\d+)/admin/info/$', views.society_admin_info, name = 'society_admin_info'),
    url(r'^society_detail/(?P<id>\d+)/admin/manager_info/$', views.society_admin_manager_info, name = 'society_admin_manager_info'),
    url(r'^society_detail/(?P<id>\d+)/admin/member_info/$', views.society_admin_member_info, name = 'society_admin_member_info'),
    url(r'^favorite_society/(?P<id>\d+)/', views.favorite_society, name = 'favorite_society'),

    url(r'^event_list/$', views.event_list, name = 'event_list'),
    url(r'^event_detail/$', views.event_detail, name = 'event_detail'),
    url(r'^event_list/ajax_search/$', views.ajax_search_event, name = 'ajax_search_event'),

    url(r'^society_search/(?P<name>[a-z_A-Z]+)/ajax_search/$', views.ajax_search_related, name = 'ajax_search_related'),
    url(r'^aboutus', views.aboutus, name = 'aboutus'),
    url(r'^ajax_counter/$', views.ajax_counter, name = 'ajax_counter'),


    ]
