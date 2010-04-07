import string, os, time
import re
import settings
from settings import MEDIA_ROOT
import csv

from django.core.files import File
from django.contrib.gis.gdal import *
from django.contrib.gis.geos import * 
        # really don't need to import et. but I am lazy today.

from core.models import *


# the folder the PDFs are in
PATH_TO_PDFS = os.path.join(settings.SITE_ROOT, '../data/files/')
# a mapping of map number (1...100-ish) to map name
PATH_TO_KEY = os.path.join(settings.SITE_ROOT, '../data/files/key.csv')
# shapefile describing cluster boundaries
PATH_TO_CLUSTERS = os.path.join(settings.SITE_ROOT, '../data/clusters/cluster_4326.shp')

def fake_slug(string):
    '''
    returns a fake slug for URL handling
    '''
    string = string.replace(" ", "_")
    return string
    
    
def fake_deslug(slug):
    slug = slug.replace("_", " ")
    return slug
    
    
def handle_uploaded_file(f):
    destination = open(os.path.join(MEDIA_ROOT, f), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    

def get_details(fname):
    # strip off '.pdf'
    fname = fname[0:-4] 
    
    results = {
        'cluster': None,
        'map': None,
        'is_appendix': False,
        'is_color': False,
        'year': None,
        'quarter': None,        
    }
    null_results = {
        'cluster': None,
        'map': None,
        'is_appendix': False,
        'is_color': False,
        'year': None,
        'quarter': None,        
    }
    
    # Find the cluster number (1 or two digits following a cap C)
    # matches 10 in C10M82
    match = re.search(r'(C)([\d]+)', fname)
    if match is not None:
        cluster = match.group(2)
        results['cluster'] = int(cluster)
    
    # Find the map number (1 or two digits following a cap M)
    # 82 matches in C10M82
    match = re.search(r'(M)([\d]+)', fname)
    if match is not None:
        map_num = match.group(2)
        results['map'] = int(map_num)
        
    # Is it an appendix? (looks for "appendix" in filename)
    appendix_match = re.search(r'Appendix', fname)
    if appendix_match is not None:
        results['is_appendix'] = True
    else: 
        results['is_appendix'] = False
        
    # Is it in color? (looks for 'color' in filename)
    color_match = re.search(r'Color', fname)
    if color_match is not None:
        results['is_color'] = True    
    else: 
        results['is_color'] = False
        
        
    # Is this file associated with a particular year or quarter?
    date_match = re.search(r'(M)([\d]+)([abcd])', fname)
    if date_match is not None:
        # extracts the c in C1M18c_09.pdf
        # and stores it as 3, for the third quarter
        quarter_ltr = date_match.group(3)
        ltr_quarter_pair = {'a': 1, 'b': 2, 'c': 3, 'd': 4 }
        results['quarter'] = ltr_quarter_pair[quarter_ltr]
        
        # looks for the 09 in C1M18c_09.pdf
        # and stores it as 9
        year_match = re.search(r'(M)([\d]+)[abcd]_([\d]+)', fname)
        if year_match is not None:
            year = year_match.group(3)
            results['year'] = int(year) + 2000
            
        if results['year'] is None:
            return null_results


    return results
    
    
def import_pdfs():
    
    # Reads the CSV key
    # this file maps the first column (map #) to the second column (map name)
    num_to_title = {}
    key_reader = csv.reader(open(PATH_TO_KEY), delimiter=',', quotechar='|')
    for row in key_reader:
        num_to_title[row[0]] = row[1]
        
    # walk through every file in the import directory
    for subdir, dirs, files in os.walk(PATH_TO_PDFS):
        for pdf_name in files:
            
            # get the map and cluster number, etc. for each.
            pdf_details = get_details(pdf_name)
            
            # make sure the file is relevant (not a metafile)
            if pdf_details['map'] is not None:
                
                print "trying " + pdf_name
                
                # create a slug from the filename
                slug = fake_slug(num_to_title[str(pdf_details['map'])])
                
                # read in the file from the file path
                pdf_path = os.path.join(PATH_TO_PDFS, pdf_name)
                in_file = open(pdf_path, 'r')
                # create a Django file object
                file_object = File(in_file) 
                                
                f = MapFile(
                   title = num_to_title[str(pdf_details['map'])],
                   slug = slug,
                   the_file = file_object,
                   cluster = pdf_details['cluster'],
                   map_num = pdf_details['map'],
                   year = pdf_details['year'],
                   quarter = pdf_details['quarter'],
                   is_appendix = pdf_details['is_appendix'],
                   is_color = pdf_details['is_color'],
                )
                                
                f.save()   
                                
            else:
                # The file is not a PDF we should import
                print "Did not save " + pdf_name
    
    return
    
    
def import_clusterinfo():
    clusters = Cluster.objects.all()
    for c in clusters:
        c.delete()
    maps = MapType.objects.all()
    for m in maps:
        m.delete()
    
    # Create the 10 clusters.
    for i in range(10):
        c = Cluster(
            cluster_id = i+1,
            title = "Cluster " + str(i+1),
        )
        c.save()
    
    # create the 99+ map types
        
    key_reader = csv.reader(open(PATH_TO_KEY), delimiter=',', quotechar='|')
    for row in key_reader:
        
        # some maps are not numbered, this gives them a null id
        if row[0] is not '':
            map_id = row[0]
        else:
            map_id = None
            
        m = MapType(
            map_id = map_id,
            slug = fake_slug(row[1]),
            title = row[1],
        )
        m.save()
        
    return

def import_cluster_shapes():
    ds = DataSource(PATH_TO_CLUSTERS)
    lyr = ds[0]
    for feat in lyr:
        cluster_num = int(feat.get('CLUSTER'))
        cluster_to_update = Cluster.objects.get(cluster_id=cluster_num)
                
        # get the WKT fror each cluster and read it in to the appropriate
        #  class type
        poly_wkt = feat.geom.wkt
        wkt_reader = WKTReader()
        poly = wkt_reader.read(poly_wkt)
        
        # sanity check -- should be:
        # <class 'django.contrib.gis.geos.polygon.Polygon'>
        # or MultiPolygon
        print feat.geom.kml
         
        mp = "foo"
        try:
            mp = MultiPolygon(poly)
        except: 
            mp = poly
       
        cluster_to_update.mpoly = mp 
        cluster_to_update.save()
     
    