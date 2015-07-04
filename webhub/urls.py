from django.conf.urls import patterns, url, include
from rest_framework import routers
from webhub import views
from peacetrack import views as peacetrack_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'revposts', views.RevPostViewSet)
router.register(r'regions', peacetrack_views.RegionViewSet)
router.register(r'sectors', peacetrack_views.SectorViewSet)
router.register(r'ptposts', peacetrack_views.PTPostViewSet)
router.register(r'projects', peacetrack_views.ProjectViewSet)
router.register(r'goals', peacetrack_views.GoalViewSet)
router.register(r'objectives', peacetrack_views.ObjectiveViewSet)
router.register(r'indicators', peacetrack_views.IndicatorViewSet)
router.register(r'outputs', peacetrack_views.OutputViewSet)
router.register(r'outcomes', peacetrack_views.OutcomeViewSet)
router.register(r'activity', peacetrack_views.ActivityViewSet)
router.register(r'measurement', peacetrack_views.MeasurementViewSet)
router.register(r'cohort', peacetrack_views.CohortViewSet)
router.register(r'volunteer', peacetrack_views.VolunteerViewSet)

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
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^edit_post/$', views.edit_post, name='edit_post'),
    url(r'^edit_post_page/$', views.edit_post_page, name='edit_post_page'),
    url(r'^view_post/(?P<post_id>\d+)$', views.view_post, name='view_post'),
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
    url(r'^testDB/$', views.testDB, name='testDB'),
)
