import pygeoip
gi = pygeoip.GeoIP('GeoLiteCity.dat')
#print(gi.country_name_by_addr('14.139.61.12'))
#print(gi.region_by_addr('14.139.61.12'))
print(gi.record_by_addr('14.139.61.12'))
print(gi.record_by_name('14.139.61.12'))
'''
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat')
def printRecord(ip):
	rec = gi.record_by_name(ip)
	city = rec['city']
	country = rec['country_name']
	longitude = rec['longitude']
	lat = rec['latitude']
	print ('[+] Address: '  + ip + ' Geo-located ' )
	print ('[+] ' +str(city)+ ', '+str(country) )
	print ('[+] Latitude: ' +str(lat)+ ', Longitude: '+ str(longitude) )

ip = '14.139.61.12'
printRecord(ip)
'''
