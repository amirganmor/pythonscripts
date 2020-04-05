import geoip2.database
#download GeoLite2-City.mmdb
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
response = reader.city('185.129.182.251')
#print(response)
print(response.country.iso_code)
print(response.country.name)
print(response.postal.code)
print(response.subdivisions.most_specific.name)
print(response.city.name)
print(response.location.latitude)
print(response.location.longitude)
