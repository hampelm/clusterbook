from django.shortcuts import render_to_response
from django.template import Context
from django.template.defaultfilters import stringfilter
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

from models import MapFile

def home(request):
    
    count = MapFile.objects.all().count()
        
    return render_to_response('home.html', { 'count': count })
