from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveImage, SaveAudio

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
        _type = request.FILES.get('type', 'image')
        _user = user_base(id=_uid)
        _url_pic = ''
        _url_pic_tn = ''
        _url_audio = ''
        
        if _type == 'image':
            (_url_pic, _url_pic_tn) = SaveImage(_file)
        elif _type == 'audio':
            _url_audio = SaveAudio(_file)
        
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng, file_type=_type, url_pic=_url_pic, url_pic_tn= _url_pic_tn, url_audio=_url_audio)
        _status.save()
        ret['id'] = _status.id
        ret['url_pic'] = _url_pic
        ret['url_pic_tn'] = _url_pic_tn 

         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'publish status withfile failed'          

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
        _max_id = request.REQUEST.get('max_id', 99999999)
        _count = status.objects.filter(pk__gt=_since_id, pk__lt=_max_id, user=_user).count()
        _statuses = status.objects.filter(pk__gt=_since_id, pk__lt=_max_id, user=_user).order_by('-id')[:100]
        _ids = []
        for s in _statuses:
            _ids.append(s.id)
              
        ret['ids'] = _ids
        ret['total_num'] = _count
        if _count > len(_ids):
            ret['hasmore'] = 1
        else:
            ret['hasmore'] = 0
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
        _max_id = request.REQUEST.get('max_id', 99999999)
        _count = status.objects.filter(pk__gt=_since_id, pk__lt=_max_id, user=_user).count()
        _statuses = status.objects.filter(pk__gt=_since_id, pk__lt=_max_id, user=_user).order_by('-id')[:10]
        _list_statuses = []
        for s in _statuses:
            _list_statuses.append(s.toJSON())
              
        ret['statuses'] = _list_statuses
        ret['total_num'] = _count
        if _count > len(_list_statuses):
            ret['hasmore'] = 1
        else:
            ret['hasmore'] = 0   
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetUserStatus failed'          

    return MyHttpResponse(ret)  
