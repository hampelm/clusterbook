from django.shortcuts import render_to_response
from django.template import Context
from django.template.defaultfilters import stringfilter
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

from models import MapFile, MapType, Cluster

def home(request):
    response = {}
    
    count = MapFile.objects.all().count()
    maps = MapType.objects.all()
    clusters = Cluster.objects.all()
    
    response['maps'] = maps
    response['clusters'] = clusters
    response['count'] = count
            
    return render_to_response('home.html', response)


def cluster(request, cluster):
    response = {}
    
    maps = MapType.objects.all().order_by('map_id')
    clusters = Cluster.objects.all()
  #  maps_in_cluster = MapFile.objects.filter(cluster=cluster).order_by('map_num')    
        
    response['maps'] = maps
    response['clusters'] = clusters
    response['cluster'] = cluster
    
    return render_to_response('cluster.html', response)


def cluster_map(request, cluster, map_id):
    response = {}

    maps = MapType.objects.all().order_by('map_id')
    clusters = Cluster.objects.all()

    map_title = MapType.objects.get(map_id=map_id).title
    
    
    # get the files assoicated with this cluster / map colletion
    files = MapFile.objects.filter(
        cluster=cluster,
        map_num=map_id, 
        appendix=False
    )
    files.order_by('year', 'quarter')
    latest = files[0]
    
    # so, if there is only one, we don't have to do anything special.
    # if there is more than one map, we need to separate older maps, 
    # appendices, color maps etc.

        

    response['maps'] = maps
    response['map_title'] = map_title
    response['clusters'] = clusters
    response['cluster'] = cluster
   # response['older_maps'] = older_maps
   # response['latest'] = latest

    return render_to_response('cluster_map.html', response)
    