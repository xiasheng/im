from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, account_thirdparty
import datetime
import json
import hashlib
import os
import sys
from django.core.cache import cache
from view_common import Random_Str, MyHttpResponse
from view_auth import GetAuthUserId, AuthException


def getAuthCode(phonenum):
    # get authcode from thirdparty
    authcode = '123456'
    return authcode

def checkAuthCode(sid, phonenum, authcode):
    authinfo = cache.get(sid)
    if authinfo is not None and authinfo['phonenum'] == phonenum and authinfo['authcode'] == authcode:
        return True
    return False

def updateAuthCodeCache(sid, phonenum, authcode='123456'):
    authinfo = {}
    authinfo['phonenum'] = phonenum
    authinfo['authcode'] = authcode
    cache.set(sid, authinfo, 300)

def checkPhoneNum(phonenum):
    if len(phonenum) != 11:
        return False
    return True	

def RegisterVerify(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _phonenum = request.POST.get('phonenum')
        if False == checkPhoneNum(_phonenum):
            ret['retcode'] = -1
            ret['info'] = 'phonenum must be 11 bit digits'
        elif len ( user_base.objects.filter(phonenum=_phonenum) ) > 0:
            ret['retcode'] = -1
            ret['info'] = 'this user already existed'
        else:
            ret['retcode'] = 0
            ret['info'] = 'use authcode to continue'
            ret['sid'] = Random_Str()
            updateAuthCodeCache(ret['sid'],_phonenum)   
    except:
        ret['retcode'] = -1
        ret['info'] = 'register user failed'

    return MyHttpResponse(ret)

def RegisterConfirm(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _phonenum = request.POST.get('phonenum')
        _authcode = request.POST.get('authcode')
        _sid = request.POST.get('sid')
        _password = hashlib.md5(request.POST.get('password')).hexdigest().upper()
        if False == checkAuthCode(_sid, _phonenum, _authcode):
            ret['retcode'] = -1
            ret['info'] = 'authcode error'
        else:
            u = user_base(phonenum=_phonenum, password=_password)
            u.save()
    except:
        ret['retcode'] = -1
        ret['info'] = 'register user failed'

    return MyHttpResponse(ret)


def GetThirdPartyAccount(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _user = user_base(id=_uid)
        _account_list = account_thirdparty.objects.filter(user=_user)
        _accounts = []
        for a in _account_list:
            _accounts.append(a.toJSON())
        ret['accounts'] = _accounts
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetThirdPartyAccount failed'          

    return MyHttpResponse(ret) 

def AddThirdPartyAccount(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _type = request.POST.get('type_tp')
        _at_tp = request.POST.get('access_token_tp')
        _uid_tp = request.POST.get('uid_tp')
        _user = user_base(id=_uid)
        _account_tp = account_thirdparty(user=_user, account_type=_type, access_token=_at_tp, uid=_uid_tp)
        _account_tp.save()
        ret['id'] = _account_tp.id
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'AddThirdPartyAccount failed'          

    return MyHttpResponse(ret)  

def DelThirdPartyAccount(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _id = request.POST.get('id')
        _user = user_base(id=_uid)
        _account = account_thirdparty.objects.get(user=_user, id=_id)
        _account.delete()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'DelThirdPartyAccount failed' 

    return MyHttpResponse(ret)

def UpdateThirdPartyAccount(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        _id = request.POST.get('id')
        _account = account_thirdparty.objects.get(user=_user, id=_id)

        _account.account_type = request.POST.get('type_tp', _account.account_type)
        _account.access_token = request.POST.get('access_token_tp', _account.access_token)
        _account.uid = request.POST.get('uid_tp', _account.uid)
        _account.save()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'UpdateThirdPartyAccount failed'          

    return MyHttpResponse(ret)