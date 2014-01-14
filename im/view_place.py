from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

from math import sin, asin, cos, radians, degrees, fabs, sqrt

EARTH_RADIUS=6371

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    global EARTH_RADIUS
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance

def GetNearByCoordinate(lat_self, lng_self, distance):
    global EARTH_RADIUS
    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)
    
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat_self))
    dlng = degrees(dlng)
    
    return (dlat, dlng)

def GetNearByUserList(request):
    ret = {'retcode': 0, 'info': 'todo'}
    try:
        _uid = GetAuthUserId(request)
        
        ret['ids'] = []
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByUserList failed'          

    return MyHttpResponse(ret)    

def GetNearByStatusList(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = float ( request.REQUEST.get('range', "10.0"))

        (dlat, dlng) = GetNearByCoordinate(_lat, _lng, _dis)
        
        _statuses = status.objects.filter(lat__gt=_lat-dlat, lat__lt=_lat+dlat, lng__gt=_lng-dlng, lng__lt=_lng+dlng)[:50]
        
        _dict_statuses = {}
        for s in _statuses:
            d = get_distance_hav(_lat, _lng, s.lat, s.lng)
            _dict_statuses[s.id] = d
        
        _sorted_statuses = sorted(_dict_statuses.items(), key = lambda e: e[1])  
        
        _list_statuses = []
        for s in _sorted_statuses:
            _list_statuses.append({s[0] : s[1]})   
                    
        ret['ids'] = _list_statuses
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except IOError:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByStatusList failed'          

    return MyHttpResponse(ret) 

def GetNearByPhotoList(request):
    ret = {'retcode': 0, 'info': 'todo'}
    try:
        _uid = GetAuthUserId(request)
        
        ret['ids'] = []
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByPhotoList failed'          

    return MyHttpResponse(ret) 