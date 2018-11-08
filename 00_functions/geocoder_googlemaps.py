"""
@ author: Manuel Martinez
@ email: manmartgarc@gmail.com

"""

import requests
import json
import time

def getmapinfo(address):
    """
    Simple function that makes requests to the Google Maps API and returns
    coordinates, and the matched address as a tuple.
    >>> getmapinfo('165 church st, new haven, ct')
    [41.354595, -72.9358, '165 CHURCH ST, NEW HAVEN, CT, 06514']
    """

    googleurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    if len(address) < 1:
        return str('Wrong address format')

    r = requests.post(googleurl, params=dict(address=address, key=apikey))
    js = json.loads(r.json())

    if js['status'] == 'OVER_QUERY_LIMIT':
        time.sleep(1)
        r = requests.post(googleurl, params=dict(address=address))
        js = json.loads(r.json())
        if js['status'] == 'OVER_QUERY_LIMIT':
            pass

    elif not js or 'status' not in js or js['status'] != 'OK':
        return (0, 0, 0)

    else:
        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        matched_address = js['results'][0]['formatted_address']

        return (lat, lng, matched_address)
