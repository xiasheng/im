from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse


def PublishStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _text = request.POST.get('text')
        _lat = request.POST.get('lat', 0.0)
        _lng = request.POST.get('lng', 0.0)
        _user = user_base(id=_uid)
        _status = status(user=_user, text=_text, lat=_lat, lng=_lng)
        _status.save()
        ret['id'] = _status.id
         
    except AuthException:
        ret['retcode'] = -1
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'publish status failed'          

    return MyHttpResponse(ret)    

def GetStatus(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _status_id = request.POST.get('id')        
        _status = status.objects.get(id=_status_id)
        ret['status'] = _status.toJSON()
         
    except AuthException:
        ret['retcode'] = -1
        ret['info'] = 'unauthorized'
    except IOError:
        ret['retcode'] = -1
        ret['info'] = 'no such status'          

    return MyHttpResponse(ret)       
