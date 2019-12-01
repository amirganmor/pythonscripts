import urllib.request, urllib.error

url = 'http://10.10.20.105'
url2 = ""
try:
    conn = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    # Return code error (e.g. 404, 501, ...)
    # ...
    print('HTTPError: {}'.format(e.code))
except urllib.error.URLError as e:
    # Not an HTTP-specific error (e.g. connection refused)
    # ...
    print('URLError: {}'.format(e.reason))
else:
    # 200
    # ...
    print('good')
