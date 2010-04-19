from types import *

from django.shortcuts import render_to_response
from django.template import Context
from django.template.defaultfilters import stringfilter
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml

from models import MapFile, MapType, Cluster
from helpers import *

def get_maps():
    maps = MapType.objects.filter(map_id__isnull=False).order_by('map_id')
    return maps

def home(request):
    response = {}
    
    count = MapFile.objects.all().count()
    maps = get_maps()
    clusters = Cluster.objects.all()
    
    response['maps'] = maps
    response['clusters'] = clusters
    response['count'] = count
            
    return render_to_response('home.html', response)


def cluster(request, cluster):
    response = {}
    
    maps = get_maps()
    clusters = Cluster.objects.all()
    
  #  maps_in_cluster = MapFile.objects.filter(cluster=cluster).order_by('map_num')    
        
    response['maps'] = maps
    response['clusters'] = clusters
    response['cluster'] = cluster
    
    return render_to_response('cluster.html', response)


def cluster_map(request, cluster, map_id):
        
    response = {}

    maps = get_maps()
    clusters = Cluster.objects.all()
    
    try:
        map_id = int(map_id)
    except:
        pass
    
    if type(map_id) is IntType:
        map_title = MapType.objects.get(map_id=map_id).title
        
        # poor coding style -- should not be duped
        appendices = MapFile.objects.filter(
            cluster=cluster,
            map_num=map_id, 
            is_appendix=True
        )
        color = MapFile.objects.filter(
            cluster=cluster,
            map_num=map_id, 
            is_color=True
        )
        files = MapFile.objects.filter(
            cluster=cluster,
            map_num=map_id, 
            is_appendix=False,
            is_color = False
        ).order_by('-year', '-quarter')
        
    else:
        map_title = MapType.objects.get(slug=map_id).title
        appendices = MapFile.objects.filter(
            cluster=cluster,
            slug=map_id, 
            is_appendix=True
        )
        color = MapFile.objects.filter(
            cluster=cluster,
            slug=map_id, 
            is_color=True
        )
        files = MapFile.objects.filter(
            cluster=cluster,
            slug=map_id, 
            is_appendix=False,
            is_color = False
        ).order_by('-year', '-quarter')
        
        
    # get the files assoicated with this cluster / map colletion
    
    
    # the newest map is the first after sorting:
    latest = files[0]
    response['latest'] = latest
        
    
    if files.count() > 1:
        # don't include the latest maps in the "archived" version.
        response['older_maps'] = files[1:]
        
    if appendices.count() > 0:
        response['appendices'] = appendices
        
    if color.count() > 0:
        response['color'] = color[0]        

    response['maps'] = maps
    response['map_title'] = map_title
    response['clusters'] = clusters
    response['cluster'] = cluster
    
    return render_to_response('cluster_map.html', response)
    
        
def cluster_all_kml(request):
    '''
    Returns KML with all clusters
    '''
    clusters = Cluster.objects.all()

    return render_to_kml('kml/clusters.kml', {'clusters': clusters })
    
    
def cluster_hilight_kml(request, cluster):
    '''
    Returns KML with all clusters, but one highlighted.
    '''
    clusters = Cluster.objects.all()
    hilight = Cluster.objects.filter(cluster_id = cluster)
    return render_to_kml('kml/hilight.kml', 
            {'clusters': clusters , 'hilight': hilight })

def cluster_single_kml(request, cluster):
    '''
    Returns KML of a single cluster
    '''
    clusters = Cluster.objects.filter(cluster_id = cluster)
    return render_to_kml('kml/clusters.kml', {'clusters': clusters })
    
