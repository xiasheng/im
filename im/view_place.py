from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status, file_status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

import lbs

def GetNearByUserList(request):
    ret = {'retcode': 0, 
           'info': 'success',
           'size' : 0,
           'hasmore' : 1,
           'users' : [],
           }
    try:
        _uid = GetAuthUserId(request)
        
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = int ( request.REQUEST.get('range', 10000))
        _page_num = int ( request.REQUEST.get('pagenum', 0))

        res = lbs.QueryUser(_lat, _lng, _dis, _page_num)
        
        _total = res['total']
        _size = res['size']
        if _total <= 10 or _size == 0:
            ret['hasmore'] = 0

        #ret['total'] = _total
        for s in res['content']:
            if _uid == s[0]:
                _size -= 1
                continue
            _user = user_base.objects.get(id=s[0])    
            ret['users'].append({'user':_user.toJSON(), 'distance':s[1]}) 
        ret['size'] = _size
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except AssertionError:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByUserList failed'          

    return MyHttpResponse(ret)    

def GetNearByStatusList(request):
    ret = {'retcode': 0, 
           'info': 'success',
           'size' : 0,
           'hasmore' : 1,
           'statuses' : [],
           }
    try:
        _uid = GetAuthUserId(request)
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = int ( request.REQUEST.get('range', 10000))
        _ts = int(request.REQUEST.get('timespan', 7200))
        _page_num = int ( request.REQUEST.get('pagenum', 0))

        res = lbs.QueryStatus(_lat, _lng, _dis, _ts, _page_num)
        
        _total = res['total']
        _size = res['size']
        if _total <= 10 or _size == 0:
            ret['hasmore'] = 0

        #ret['total'] = _total
        for s in res['content']:
            ret['statuses'].append({'sid':s[0], 'distance':s[1]}) 
        ret['size'] = _size

    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'GetNearByStatusList failed'          

    return MyHttpResponse(ret) 


def GetNearByStatusDetail(request):
    ret = {'retcode': 0, 
           'info': 'success',
           'total': 0,
           'size' : 0,
           'hasmore' : 1,
           }
    try:
        _uid = GetAuthUserId(request)
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = int ( request.REQUEST.get('range', 10000))
        _ts = int(request.REQUEST.get('timespan', 7200))
        _page_num = int ( request.REQUEST.get('pagenum', 0))

        res = lbs.QueryStatus(_lat, _lng, _dis, _ts, _page_num)
        
        _total = res['total']
        _size = res['size']
        if _total <= 10 or _size == 0:
            ret['hasmore'] = 0

        sids = []
        distances = []
        for s in res['content']:
            sids.append(s[0])
            distances.append(s[1])
        _statuses = status.objects.filter(pk__in=sids)

        _list_statuses = []
        i = 0
        for s in _statuses:
            if _uid == s.user.id:
                _size -= 1
                continue
            _s = s.toJSON()
            _s['distance'] = distances[i]
            _list_statuses.append(_s)
            i += 1
                    
        ret['statuses'] = _list_statuses
        #ret['total'] = _total
        ret['size'] = _size
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByStatusDetail failed'          

    return MyHttpResponse(ret) 


def GetNearByPhotoList_LBS(request):
    ret = {'retcode': 0, 
           'info': 'success',
           'size' : 0,
           'hasmore' : 1,
           }
    try:
        _uid = GetAuthUserId(request)
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = int ( request.REQUEST.get('range', 10000))
        _ts = int(request.REQUEST.get('timespan', 7200))
        _page_num = int ( request.REQUEST.get('page_num', 0))
        _type = 2

        res = lbs.QueryStatus(_lat, _lng, _dis, _ts, _page_num, _type)
        
        _total = res['total']
        _size = res['size']
        if _total <= 10 or _size == 0:
            ret['hasmore'] = 0

        sids = []
        distances = []
        for s in res['content']:
            sids.append(s[0])
            distances.append(s[1])
        _photos = file_status.objects.filter(status__in=sids)

        _list_photos = []
        i = 0
        for s in _photos:
            _s = s.toJSON()
            _s['distance'] = distances[i]
            _list_photos.append(_s)
            i += 1
                    
        ret['photos'] = _list_photos
        #ret['total'] = _total
        ret['size'] = _size
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'GetNearByPhotoList failed'          

    return MyHttpResponse(ret)


def GetNearByPhotoList(request):
    ret = {'retcode': 0, 
           'info': 'success',
           'size' : 0,
           'hasmore' : 1,
           }
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        _page_num = int ( request.REQUEST.get('pagenum', 0))
        _statuses = status.objects.filter(type=2).exclude(user=_user).order_by('-id')[_page_num*10:(_page_num+1)*10]
        _photos = []
        for s in _statuses:
            _photos.append(s.toJSON2())
              
        ret['photos'] = _photos
        ret['size'] = len(_photos)
        ret['pagenum'] = _page_num
        if 10 == len(_photos):
            ret['hasmore'] = 1
        else:
            ret['hasmore'] = 0
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByPhotoList failed'          

    return MyHttpResponse(ret)    