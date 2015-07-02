#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.conf.urls import patterns, url, include
from rest_framework import routers
from webhub import views as webhub_views
from peacetrack import views

urlpatterns = patterns('',
    url(r'^$', views.peacetrack, name='peacetrack'),
    url(r'^malaria/$', webhub_views.malaria, name='malaria'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^api/', include(router.urls)),
    url(r'^volunteer/$', views.volunteer, name='volunteer'),
    url(r'^summary/$', views.summary, name='summary'),
)





