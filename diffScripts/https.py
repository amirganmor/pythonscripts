import requests
import urllib.request
import os, ssl
import http.client
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context
    
'''    
r = urllib.request.urlopen('https://52.91.188.26/')
conn = http.client.HTTPSConnection('52.91.188.26', 443)
conn.putrequest('GET', '/')
conn.endheaders() # <---
r = conn.getresponse()
print(r.read())
'''

r = urllib.request.urlopen(https://52.91.188.26/')
print(r.read())
