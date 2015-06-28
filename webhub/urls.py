#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.conf.urls import patterns, url, include
from rest_framework import routers
from webhub import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'revposts', views.RevPostViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'sectors', views.SectorViewSet)
router.register(r'ptposts', views.PTPostViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'objectives', views.ObjectiveViewSet)
router.register(r'indicators', views.IndicatorViewSet)
router.register(r'outputs', views.OutputViewSet)
router.register(r'outcomes', views.OutcomeViewSet)
router.register(r'activity', views.ActivityViewSet)
router.register(r'measurement', views.MeasurementViewSet)
router.register(r'cohort', views.CohortViewSet)
router.register(r'volunteer', views.VolunteerViewSet)

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^signup_page/$', views.signup_page, name='signup_page'),
    url(r'^signup_do/$', views.signup_do, name='signup_do'),
    url(r'^send_verification_email/$', views.send_verification_email, name='send_verification_email'),
    url(r'^send_email/$', views.send_email, name='send_email'),
    url(r'^login_do/$', views.login_do, name='login_do'),
    url(r'^logout_do/$', views.logout_do, name='logout_do'),
    url(r'^malaria/$', views.malaria, name='malaria'),
    url(r'^peacetrack/$', views.peacetrack, name='peacetrack'),
    #url(r'^post_form/$', views.post_form, name='post_form'),
    url(r'^post_new/$', views.post_new, name='post_new'),
    url(r'^edit_post/$', views.edit_post, name='edit_post'),
    url(r'^edit_post_page/$', views.edit_post_page, name='edit_post_page'),
    url(r'^view_post/$', views.view_post, name='view_post'),
    url(r'^delete_post/$', views.delete_post, name='delete_post'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^edit_profile_page/$', views.edit_profile_page, name='edit_profile_page'),
    url(r'^forgot_pass_page/$', views.forgot_pass_page, name='forgot_pass_page'),
    url(r'^forgot_pass/$', views.forgot_pass, name='forgot_pass'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^reset_pass_page/$', views.reset_pass_page, name='reset_pass_page'),
    url(r'^change_pass/$', views.change_pass, name='change_pass'),
    url(r'^change_pass_page/$', views.change_pass_page, name='change_pass_page'),
    url(r'^pcuser/$', views.pcuser_list, name='pcuser_list'),
    url(r'^revpost/$', views.revpost_list, name='revpost_list'),
    url(r'^pcuser/(?P<pk>[0-9]+)/$', views.pcuser_detail, name='pcuser_detail'),
    url(r'^revpost/(?P<pk>[0-9]+)/$', views.revpost_detail, name='revpost_detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^aboutPC/$', views.aboutPC, name='aboutPC'),
    url(r'^policies/$', views.policies, name='policies'),
    url(r'^details/$', views.details, name='details'),
    url(r'^helpPC/$', views.helpPC, name='helpPC'),
    url(r'^volunteer/$', views.volunteer, name='volunteer'),
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^testDB/$', views.testDB, name='testDB'),
    #url(r'^post/$', views.post_list, name='post_list'),
    #url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
)
