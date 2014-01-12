from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS=6371           # 地球平均半径，6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    global EARTH_RADIUS
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance

def GetNearByCoordinate(lng_self, lat_self, distance):
    global EARTH_RADIUS
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat))
    dlng = degrees(dlng)

    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)
    retun (dlng, dlat)

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
    ret = {'retcode': 0, 'info': 'todo'}
    try:
        _uid = GetAuthUserId(request)
        _lng = request.REQUEST.get('lng')
        _lat = request.REQUEST.get('lat')

        (dlng, dlat) = GetNearByCoordinate(_lng, _lat)
        
        ret['ids'] = []
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
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