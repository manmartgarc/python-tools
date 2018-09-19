"""
@author: Manuel Martinez
@email: manmartgarc@gmail.com

This script defines a function which takes an address or a lat/lon pair as
an input and returns the following:
    1)  Latitude
    2)  Longitude
    3)  Matched address

"""

import urllib.request, urllib.parse, urllib.error
import json
import time

def getmapinfo(address):

    googleurl = 'http://maps.googleapis.com/maps/api/geocode/json?'

    if len(address) < 1:
        return str('Wrong address format')

    url = googleurl + urllib.parse.urlencode({'address': address})

    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    if js['status'] == 'OVER_QUERY_LIMIT':
        time.sleep(1)
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)
        if js['status'] == 'OVER_QUERY_LIMIT':
            pass

    elif not js or 'status' not in js or js['status'] != 'OK':
        return (0,0,0)

    else:
        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        matched_address = js['results'][0]['formatted_address']
