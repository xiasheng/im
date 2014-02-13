from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status, file_status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile
import lbs
import thread

def PublishStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _text = request.REQUEST.get('text', '')
        _lat = float (request.REQUEST.get('lat', 0.0))
        _lng = float (request.REQUEST.get('lng', 0.0))
        _user = user_base(id=_uid)
        _stype = 1
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng)
        _status.save()
        ret['id'] = _status.id
        if _lat > 0 and _lng > 0:
            thread.start_new_thread(lbs.UploadStatus, (_status.id, _lat, _lng, _stype))
         
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
        _lat = float (request.REQUEST.get('lat', 0.0))
        _lng = float (request.REQUEST.get('lng', 0.0))
        _file = request.FILES.get('file')
        _type = request.FILES.get('type', 'image')
        _user = user_base(id=_uid)
        _url_pic = ''
        _url_pic_tn = ''
        _url_audio = ''
        
        if _type == 'image':
            _stype = 2
            (_fid, _url_pic, _url_pic_tn) = SaveFile(_file, 'StatusImage')
        elif _type == 'audio':
            _stype = 3
            (_fid, _url_audio, _url_null)  = SaveFile(_file, 'StatusAudio')
        
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng, type=_stype)
        _status.save()
        _file_status = file_status(user=_user, status=_status, fid=_fid, file_type=_type, url_pic=_url_pic, url_pic_tn= _url_pic_tn, url_audio=_url_audio)
        _file_status.save()

        ret['id'] = _status.id
        ret['url_pic'] = _url_pic
        ret['url_pic_tn'] = _url_pic_tn 
        ret['fid'] = _fid
        if _lat > 0 and _lng > 0:
            thread.start_new_thread(lbs.UploadStatus, (_status.id, _lat, _lng, _stype))
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
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
