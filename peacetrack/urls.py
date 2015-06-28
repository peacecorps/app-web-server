#Version : Phython/Django 2.7.6, PostgreSQL 9.3.4
#Author : Vaibhavi Desai
#Github username : desaivaibhavi
#email : ranihaileydesai@gmail.com

from django.conf.urls import patterns, url, include
from rest_framework import routers
from webhub import views as webhub_views
from peacetrack import views



router = routers.DefaultRouter()
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
    url(r'^$', views.peacetrack, name='peacetrack'),
    url(r'^malaria/$', webhub_views.malaria, name='malaria'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^api/', include(router.urls)),
    url(r'^volunteer/$', views.volunteer, name='volunteer'),
    url(r'^summary/$', views.summary, name='summary'),
)





