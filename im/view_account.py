from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base
import datetime
import json
import hashlib
import os
import sys
from django.core.cache import cache
from view_common import Random_Str, MyHttpResponse


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
