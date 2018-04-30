from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^show_reg$', views.show_reg),
    url(r'^post/(?P<user_id>\d+)$', views.post),
    url(r'^follow/(?P<leader_id>\d+)$', views.follow),
    url(r'^show$', views.show),
    url(r'^show_user/(?P<user_id>\d+)$', views.show_user),
    url(r'^show_all$', views.show_all),
    url(r'^show_followers$', views.show_followers),
    url(r'^show_inbox/(?P<leader_id>\d+)$', views.show_inbox),
    url(r'^send_message/(?P<leader_id>\d+)/(?P<user_id>\d+)$', views.send_message),
    url(r'^show_user_inbox/(?P<user_id>\d+)$', views.show_user_inbox),
    url(r'^delete_follows$', views.delete_follows),
    url(r'^delete_posts$', views.delete_posts),
    url(r'^delete_all$', views.delete_all),
    url(r'^delete_inbox$', views.delete_inbox)
]
