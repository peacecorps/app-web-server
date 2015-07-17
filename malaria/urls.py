from django.conf.urls import patterns, url
from malaria import views

urlpatterns = patterns(
    '',
    url(r'^create_post/$',
        views.create_post,
        name='create_post'),
    url(r'^delete_post/(?P<post_id>\d+)$',
        views.delete_post,
        name='delete_post'),
    url(r'^edit_post/(?P<post_id>\d+)$',
        views.edit_post,
        name='edit_post'),
    url(r'^list_posts/$',
        views.list_posts,
        name='list_posts'),
    url(r'^revpost/$',
        views.revpost_list,
        name='revpost_list'),
    url(r'^revpost/(?P<pk>[0-9]+)/$',
        views.revpost_detail,
        name='revpost_detail'),
    url(r'^view_post/(?P<post_id>\d+)$',
        views.view_post,
        name='view_post'),
)
