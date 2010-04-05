from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from core import views

urlpatterns = patterns('',
    (r'^$',  views.home),
    (r'^cluster/(?P<cluster>\d+)/$', views.cluster),
    (r'^cluster/(?P<cluster>\d+)/map/(?P<map_id>\d+)/$', views.cluster_map),
    
)