#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.conf.urls import patterns, url

from webhub import views

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login_do/$', views.login_do, name='login_do'),
    url(r'^logout_do/$', views.logout_do, name='logout_do'),
    url(r'^malaria/$', views.malaria, name='malaria'),
    url(r'^peacetrack/$', views.peacetrack, name='peacetrack'),
    url(r'^post_form/$', views.post_form, name='post_form'),
    url(r'^post_new/$', views.post_new, name='post_new'),
    url(r'^edit_post/$', views.edit_post, name='edit_post'),
    url(r'^edit_post_page/$', views.edit_post_page, name='edit_post_page'),
    url(r'^view_post/$', views.view_post, name='view_post'),
    url(r'^delete_post/$', views.delete_post, name='delete_post'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_profile_page/$', views.edit_profile_page, name='edit_profile_page'),
)




