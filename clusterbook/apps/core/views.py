from django.shortcuts import render_to_response
from django.template import Context
from django.template.defaultfilters import stringfilter
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms

def home(request):
        
    return render_to_response('home.html', {  })
