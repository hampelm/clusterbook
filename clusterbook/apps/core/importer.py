from core.models import *

import string, os, time
import re
import settings
from settings import MEDIA_ROOT
import csv

from django.core.files import File

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
        
    # Is it in color? (looks for 'color' in filename)
    appendix_match = re.search(r'Color', fname)
    if appendix_match is not None:
        results['is_color'] = True    
    
    return results
    
    
def import_pdfs():
    path_to_pdfs = os.path.join(settings.SITE_ROOT, '../data/files/')
    path_to_key = os.path.join(settings.SITE_ROOT, '../data/files/key.csv')
    
    # Reads the CSV key
    # this file maps the first column (map #) to the second column (map name)
    num_to_title = {}
    key_reader = csv.reader(open(path_to_key), delimiter=',', quotechar='|')
    for row in key_reader:
        num_to_title[row[0]] = row[1]
        
    # walk through every file in the import directory
    for subdir, dirs, files in os.walk(path_to_pdfs):
        for pdf_name in files:
            
            # get the map and cluster number, etc. for each.
            pdf_details = get_details(pdf_name)
            
            # make sure the file is relevant (not a metafile)
            if pdf_details['map'] is not None:
                
                print "trying " + pdf_name
                
                # create a slug from the filename
                slug = fake_slug(num_to_title[str(pdf_details['map'])])
                
                # read in the file from the file path
                pdf_path = os.path.join(path_to_pdfs, pdf_name)
                in_file = open(pdf_path, 'r')
                # create a Django file object
                file_object = File(in_file) 
                                
                f = MapFile(
                   title = num_to_title[str(pdf_details['map'])],
                   slug = slug,
                   the_file = file_object,
                   cluster = pdf_details['cluster'],
                   map_num = pdf_details['map'],
                )
                                
                f.save()   
                                
            else:
                # The file is not a PDF we should import
                print "Did not save " + pdf_name
    
    return
    