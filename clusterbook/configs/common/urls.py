from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),

 #   (r'^$', 'django.views.generic.simple.redirect_to', { 'url': '/core/'}),
    
    (r'^', include('core.urls')),
    
#    include('core.urls')
)