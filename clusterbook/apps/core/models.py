from django.contrib.gis.db import models

# Create your models here.
class MapFile(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=256)
    narrative = models.TextField(null=True)
    
    cluster = models.IntegerField(max_length = 2, null=True)
    map_num = models.IntegerField(max_length = 3, null=True)
    
    # a method for keeping track of the most recent file
    latest = models.NullBooleanField(null=True) 
    year = models.IntegerField(max_length = 2, null=True) # eg 08 09 ...
    quarter = models.IntegerField(max_length = 1, null=True) # eg 1, 2, 3, 4
    
    is_appendix = models.NullBooleanField(null=True) 
    is_color = models.NullBooleanField(null=True) 
    
    date_posted = models.DateTimeField(auto_now=True)
    
    the_file = models.FileField("File", upload_to='pdfs')
#    thumbnail = models.ImageField("Thumbnail", upload_to='images/thumbs')
#    image = models.ImageField("Image", upload_to='images/')
    
    scribd_id = models.CharField(max_length=100, null=True)
    scribd_link = models.CharField(max_length=256, null=True)
    scribd_ak = models.CharField(max_length=256, null=True)
    
    
class Cluster(models.Model):
    cluster_id = models.IntegerField(max_length = 2, null=True)
    title = models.CharField(max_length=100)
    narrative = models.TextField(null=True)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField(null=True) # uses srid = 4326
    objects = models.GeoManager()
    
    
class MapType(models.Model):
    map_id = models.IntegerField(max_length = 3, null=True)
    title = models.CharField(max_length=100)
  #  slug = models.SlugField(max_length=256)
    narrative = models.TextField(null=True)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField(null=True) # uses srid = 4326
    objects = models.GeoManager()
    
        