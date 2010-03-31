"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
import importer

class ImportTest(TestCase):
    def test_simple(self):
        fname = "C10M82.pdf"
        good_results = {
            'cluster': 10,
            'map': 82,
            'is_appendix': False,
            'is_color': False,
            'year': None,
            'quarter': None,        
        }
        results = importer.get_details(fname)
        self.failUnlessEqual(good_results, results)

    def test_appendix(self):
        fname = "C10M48AppendixA.pdf"
        
        good_results = {
            'cluster': 10,
            'map': 48,
            'is_appendix': True,
            'is_color': False,
            'year': None,
            'quarter': None,        
        }
        results = importer.get_details(fname)
        self.failUnlessEqual(good_results, results)
        
        
        
        

