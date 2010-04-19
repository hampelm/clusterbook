import string, os, time

def fake_slug(string):
    '''
    returns a fake slug for URL handling
    '''
    string = string.replace(" ", "_")
    return string
    
    
def fake_deslug(slug):
    slug = slug.replace("_", " ")
    return slug
