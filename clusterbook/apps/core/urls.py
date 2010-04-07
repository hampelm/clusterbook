from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from core import views

urlpatterns = patterns('',
    (r'^$',  views.home),
    (r'^cluster/(?P<cluster>\d+)/$', views.cluster),
    (r'^cluster/(?P<cluster>\d+)/map/(?P<map_id>\d+)/$', views.cluster_map),
    
    (r'^kml/all$', views.cluster_all_kml),
    (r'^kml/(?P<cluster>\d+)/hilight$', views.cluster_hilight_kml),
    (r'^kml/(?P<cluster>\d+)/single$', views.cluster_single_kml),
    
    
)