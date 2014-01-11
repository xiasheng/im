from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_history
import datetime
import hashlib
from django.core.cache import cache
from view_common import Random_Str, MyHttpResponse
import logging 

class AuthException(Exception):
    def __init__(self, msg='unauthorized'):
        self.msg = msg

def gennrateToken(phonenum, uid):
    tokens = {}
    access_token = Random_Str()
    refresh_token = Random_Str()    
    tokens['at'] = access_token
    tokens['rt'] = refresh_token
    tokens['pn'] = phonenum
    tokens['uid'] = uid
    logging.info('set cache %s' %access_token)
    cache.set(access_token, tokens, 3600)
    return tokens
    

def Login(request):
    ret = {'retcode': 0, 'info': 'success'}   
  
    try:
        _phonenum = request.POST.get('phonenum')
        _password = hashlib.md5(request.POST.get('password')).hexdigest().upper()
        _source = request.POST.get('source', 'Android')
        _ip_addr = request.POST.get('ip_addr', '127.0.0.1')
        _lat = request.POST.get('lat', 0.0)
        _lng = request.POST.get('lng', 0.0)
        
        _user = user_base.objects.get(phonenum=_phonenum, password=_password)
        
        #update user history
        user_history.objects.create(user=_user, source=_source, ip_addr=_ip_addr, lat=_lat, lng=_lng)
        tokens = gennrateToken(_phonenum, _user.id)
        ret['access_token'] = tokens['at']
        ret['refresh_token'] = tokens['rt']

    except:
        ret['retcode'] = -1
        ret['info'] = 'login failed'

    return MyHttpResponse(ret)

def Logout(request):
    ret = {'retcode': 0, 'info': 'success'}

    try:
        _phonenum = request.POST.get('phonenum')    
        _access_token = request.POST.get('access_token')
        tokens = cache.get(_access_token)           

        if tokens['pn'] == _phonenum:
            cache.delete(_access_token)
                        
    except:
        pass

    return MyHttpResponse(ret)

def ExternalAuth(request):
    ret = {'retcode': 0, 'info': 'success'}

    try:
        _phonenum = request.POST.get('name')
        _password = hashlib.md5(request.POST.get('password')).hexdigest().upper()
        u = user_base.objects.get(phonenum=_phonenum, password=_password)
    except:
        ret['retcode'] = -1
        ret['info'] = 'auth failed'

    return MyHttpResponse(ret)
    
def GetAuthUserId(request):
    try:
        _access_token = request.POST.get('access_token')
        tokens = cache.get(_access_token)
        return tokens['uid']  
    except:                     
        raise AuthException('')