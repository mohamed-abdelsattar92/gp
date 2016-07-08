import urllib.request
import pandas

# test the get visits lists url
# url = "http://localhost:8000/api/technician/3/visits"
url = "http://maps.googleapis.com/maps/api/geocode/json?address=new%20york&sensor=false"

obj =  urllib.request.urlopen(url)

obj_json = pandas.read_json(obj)
print(obj_json)
obj_json['results'][0]
