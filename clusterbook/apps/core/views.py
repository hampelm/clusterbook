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
    ca = models.CommunityArea.objects.get(area_number=area_number)
    return render_to_kml('core/community_area.kml', {'comm_area': ca })
    
    
def cluster_hilight_kml(request, cluster_to_highlight):
    '''
    Returns KML with all clusters, but one highlighted.
    '''
    ca = models.CommunityArea.objects.get(area_number=area_number)
    return render_to_kml('core/community_area.kml', {'comm_area': ca })

def cluster_single_kml(request, cluster):
    '''
    Returns KML of a single cluster
    '''
    ca = models.CommunityArea.objects.get(area_number=area_number)
    return render_to_kml('core/community_area.kml', {'comm_area': ca })
    
