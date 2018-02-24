
# coding: utf-8

# In[143]:


# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db
from Api import app
class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_api_adding(self):
        datap= { "pin": "110085", "place_name": "Rohini", "admin_name": "Delhi", "latitude": "28.749472", "longitude": "77.056533" }
        res = self.client.post('/post_location',data=json.dumps(datap),content_type='application/json')
        self.assertEqual(res.status_code, 200)
        print '-> /post_location : result - '+res.data
        #self.assertIn('POSTING DATA', str(res.data))

    def test_api__get_postgres(self):
        # API /get_using_postgres
        res = self.client.get('/get_using_postgres?latitude=28.749472&longitude=77.056533')
        self.assertEqual(res.status_code, 200)
        print '-> /get_using_postgres : result - '+res.data
        #API /get_using_self
    def test_api__get_self(self):
        res = self.client.get('/get_using_self?latitude=28.749472&longitude=77.056533')
        self.assertEqual(res.status_code, 200)
        print '-> /get_using_self : result - '+res.data
        #API /get_place
    def test_api__get_location(self):
        res = self.client.get('/get_place?latitude=28.749472&longitude=77.056533')
        self.assertEqual(res.status_code, 200)
        print '-> /get_place : result - '+res.data



 
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

