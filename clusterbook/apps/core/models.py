from django.db import models

# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    narrative = models.TextField(null=True)
    
    cluster = models.IntegerField(max_length = 2, null=True)
    map_num = models.IntegerField(max_length = 2, null=True)
    
    is_appendix = models.BooleanField(null=True) 
    is_color = models.BooleanField(null=True) 
    
    date_posted = models.DateTimeField(auto_now=True)
    
    the_file = models.FileField("File", upload_to='pdfs')
    scribd_id = models.CharField(max_length=100, null=True)
    scribd_link = models.CharField(max_length=256, null=True)
    scribd_ak = models.CharField(max_length=256, null=True)
    