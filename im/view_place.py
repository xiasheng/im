from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

import lbs


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
    ret = {'retcode': 0, 
           'info': 'success',
           'total': 0,
           'size' : 0,
           'hasmore' : 1,
           'content' : {},
           }
    try:
        _uid = GetAuthUserId(request)
        _lat = float ( request.REQUEST.get('lat') )
        _lng = float ( request.REQUEST.get('lng') )
        _dis = float ( request.REQUEST.get('range', 10000))
        _page_num = int ( request.REQUEST.get('page_num', 0))

        res = lbs.Query(_dis, _lat, _lng, _page_num)
        
        _total = res['total']
        _size = res['size']
        if _size < 10:
            ret['hasmore'] = 0

        ret['total'] = _total
        ret['size'] = _size
        ret['content'] = res['content']
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
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
        _dis = float ( request.REQUEST.get('range', 10000))
        _ts = int(request.REQUEST.get('timespan', 7200))
        _page_num = int ( request.REQUEST.get('page_num', 0))

        res = lbs.Query(_lat, _lng, _dis, _ts, _page_num)
        
        _total = res['total']
        _size = res['size']
        if _size < 10:
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
        ret['total'] = _total
        ret['size'] = _size
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except IOError:
        ret['retcode'] = -1
        ret['info'] = 'GetNearByStatusDetail failed'          

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