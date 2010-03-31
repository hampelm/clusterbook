from core.models import *

import string, os, time
import re
import settings
import csv

def fake_slug(string):
    '''
    returns a fake slug for URL handling
    '''
    string = string.replace(" ", "_")
    return string
    
    
def fake_deslug(slug):
    slug = slug.replace("_", " ")
    return slug
    

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
    # maps the first column (map #) to the second column (map name)
    num_to_title = {}
    key_reader = csv.reader(open(path_to_key), delimiter=',', quotechar='|')
    for row in key_reader:
        num_to_title[row[0]] = row[1]
        
        
    for subdir, dirs, files in os.walk(path_to_pdfs):
        for pdf in files:
            results = get_details(pdf)
            
            
            
            f = File(
               title = num_to_title[results[map_num]]
               slug = fake_slug(num_to_title[results[map_num]])
               
               cluster = results[cluster]
               map_num = results[map_num]
               the_file = pdf                
            )
            
            f.save()

