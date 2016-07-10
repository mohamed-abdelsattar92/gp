import urllib.request
import urllib
import pandas
import json

# test the get visits lists url
# url = "http://localhost:8000/api/technician/3/visits"
# url = "http://maps.googleapis.com/maps/api/geocode/json?address=new%20york&sensor=false"

url = "https://maps.googleapis.com/maps/api/directions/json?origin=30.0690726399142,31.264596810559055&destination=30.069778295177866,31.28094755671384&waypoints=optimize:true|30.062015810546768,31.266828408459446|30.064875744134433,31.274767747143528|30.069666876260232,31.280775895336888|30.054066989775723,31.2560137417114"

obj =  urllib.request.urlopen(url)

# print(type(obj))
#
# print(obj.read().decode(encoding='UTF-8'))
#
json_obj = json.loads(obj.read().decode(encoding='UTF-8'))

print(json_obj['routes'][0]['waypoint_order'])
