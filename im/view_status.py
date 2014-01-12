from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

def PublishStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _text = request.REQUEST.get('text')
        _lat = request.REQUEST.get('lat', 0.0)
        _lng = request.REQUEST.get('lng', 0.0)
        _user = user_base(id=_uid)
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng)
        _status.save()
        ret['id'] = _status.id
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'publish status failed'          

    return MyHttpResponse(ret)    

def PublishStatusWithFile(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _text = request.REQUEST.get('text')
        _lat = request.REQUEST.get('lat', 0.0)
        _lng = request.REQUEST.get('lng', 0.0)
        _file = request.FILES.get('file')
        _type = request.FILES.get('type', '')
        _user = user_base(id=_uid)

        _fid = SaveFile(_file)
        
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng, file_id=_fid, file_type=_type)
        _status.save()
        ret['id'] = _status.id
        ret['fid'] = _fid 

         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'publish status failed'          

    return MyHttpResponse(ret)  

def GetStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _status_id = request.REQUEST.get('id')        
        _status = status.objects.get(id=_status_id)
        ret['status'] = _status.toJSON()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'no such status'          

    return MyHttpResponse(ret)       
    
def BatchGetStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _status_ids = request.REQUEST.get('ids', []).split(',') 
        _statuses = status.objects.filter(pk__in=_status_ids)
        _list_statuses = []
        for s in _statuses:
            _list_statuses.append(s.toJSON())
              
        ret['statuses'] = _list_statuses
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'no such status'          

    return MyHttpResponse(ret) 
    
def GetUserStatusList(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid_self = GetAuthUserId(request)
        _uid = request.REQUEST.get('uid', _uid_self)
        _user = user_base(id=_uid)
        _since_id = request.REQUEST.get('since_id', 0)
        _statuses = status.objects.filter(pk__gte=_since_id, user=_user)[:100]
        _ids = []
        for s in _statuses:
            _ids.append(s.id)
              
        ret['ids'] = _ids
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetUserStatus failed'          

    return MyHttpResponse(ret)     

def GetUserStatusDetail(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid_self = GetAuthUserId(request)
        _uid = request.REQUEST.get('uid', _uid_self)        
        _user = user_base(id=_uid)
        _since_id = request.REQUEST.get('since_id', 0)
        _statuses = status.objects.filter(pk__gte=_since_id, user=_user)[:10]
        _list_statuses = []
        for s in _statuses:
            _list_statuses.append(s.toJSON())
              
        ret['statuses'] = _list_statuses
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetUserStatus failed'          

    return MyHttpResponse(ret)  
