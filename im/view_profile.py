from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_profile, user_profile_photowall
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse
from view_file import SaveProfileImage

def AddProfile(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        
        _num = user_profile.objects.filter(user=_user).count()
        if _num >= 3:
          ret['retcode'] = -1
          ret['info'] = 'profile num exceeds'
          return MyHttpResponse(ret)     
          
        _name = request.REQUEST.get('name', '')
        _gender = request.REQUEST.get('gender', '')
        _age = int (request.REQUEST.get('age', 0))
        _addr = request.REQUEST.get('addr', '')
        _category = request.REQUEST.get('category', '')
        _isDefault = int (request.REQUEST.get('isDefault', 0))

        _profile = user_profile(user=_user, name=_name, gender=_gender, age=_age, addr=_addr, category=_category)
        _profile.save()
        ret['id'] = _profile.id
        
        if _isDefault == 1:
          _user.update(default_profile_id=_profile.id)
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'AddProfile failed'          

    return MyHttpResponse(ret) 

def DelProfile(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _pid = request.REQUEST.get('pid')
        _user = user_base(id=_uid)

        user_profile.objects.get(user=_user, id=_pid).delete()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'DelProfile failed'          

    return MyHttpResponse(ret)


def UpdateProfile(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        
        _pid = request.REQUEST.get('pid')
        _profile = user_profile.objects.get(user=_user, id=_pid)
          
        _name = request.REQUEST.get('name', _profile.name)
        _gender = request.REQUEST.get('gender', _profile.gender)
        _age = int (request.REQUEST.get('age', _profile.age))
        _addr = request.REQUEST.get('addr', _profile.addr)
        _category = request.REQUEST.get('category', _profile.category)
        
        _isDefault = int (request.REQUEST.get('isDefault', 0))

        _profile = user_profile.objects.filter(user=_user, id=_pid).update(name=_name, gender=_gender, age=_age, addr=_addr, category=_category)
                
        if _isDefault == 1:
          user_base.objects.filter(id=_uid).update(default_profile_id=_pid)
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'UpdateProfile failed'          

    return MyHttpResponse(ret) 

def ShowProfile(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base.objects.get(id=_uid)
        
        _profiles = user_profile.objects.filter(user=_user)
          
        _list_profiles = []
        for p in _profiles:
            pp = p.toJSON()
            
            if p.id == _user.default_profile_id:
                pp['isDefault'] = 1
            else:
                pp['isDefault'] = 0    
            _list_profiles.append(pp)
              
        ret['profiles'] = _list_profiles
        ret['num_fans'] = 0
        ret['num_friends'] = 0
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'ShowProfile failed'          

    return MyHttpResponse(ret) 

def UploadProfileImage(request):
    ret = {'retcode': 0, 'info': 'success'}   
  
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        _file = request.FILES.get('file')
        _pid = request.REQUEST.get('pid')
        
        _profile = user_profile.objects.filter(user=_user, id=_pid)
        if len(_profile) == 1:
            _url_image = SaveProfileImage(_file)
            ret['url_image'] = _url_image
            _profile.update(url_image=_url_image)
        else:
            ret['retcode'] = -1
            ret['info'] = 'no such profile'
            return MyHttpResponse(ret)
             
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'auth failed'
    except :
        ret['retcode'] = -1
        ret['info'] = 'UploadProfileImage failed'

    return MyHttpResponse(ret)