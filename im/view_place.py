from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveFile

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