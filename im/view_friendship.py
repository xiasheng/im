from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_profile, friends
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse

def AddFriend(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        
        _fid = request.REQUEST.get('fid')
        
        _count = friends.objects.filter(user=_user, friend_id=_fid).count()
        if _count == 0:
          _friend = friends.objects.create(user=_user, friend_id=_fid)
          
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'AddFriend failed'          

    return MyHttpResponse(ret) 

def DelFriend(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        _fid = request.REQUEST.get('fid')

        friends.objects.filter(user=_user, friend_id=_fid).delete()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'DelFriend failed'          

    return MyHttpResponse(ret)


def ShowFriends(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _userid = request.REQUEST.get('id', _uid)
        _user = user_base(id=_userid)
        _friends = friends.objects.filter(user=_user)
        _fids = []
        
        for f in _friends:
            _fids.append(f.friend_id)    
        
        _users = user_base.objects.filter(pk__in=_fids)   
        _friends = []
        for u in _users:
            _friends.append(u.toJSON()) 
                    
        ret['friends'] = _friends      
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'ShowFriends failed'          

    return MyHttpResponse(ret)

def ShowFans(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _userid = request.REQUEST.get('id', _uid)
        _user = user_base(id=_userid)
        _fans = friends.objects.filter(friend_id=_userid)
        _fids = []
        
        for f in _fans:
            _fids.append(f.user.id)    
        
        _users = user_base.objects.filter(pk__in=_fids)   
        _fans = []
        for u in _users:
            _fans.append(u.toJSON()) 
                    
        ret['fans'] = _fans      
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'ShowFans failed'          

    return MyHttpResponse(ret)


def SearchFriends(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _user = user_base(id=_uid)
        
        _type = request.REQUEST.get('type','name')
        _q = request.REQUEST.get('q')
        
        result = []
        if _type == 'name':
            _users = user_profile.objects.filter(name=_q)
            for u in _users:
                if u.user.id == _uid:
                    continue
                result.append(u.toJSONBasic()) 
        elif _type == 'id':
            _users = user_base.objects.filter(phonenum=_q)
            for u in _users:
                if u.id == _uid:
                    continue
                result.append(u.toJSON()) 
        else:
            pass  
                    
        ret['users'] = result      
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'SearchFriends failed'          

    return MyHttpResponse(ret)

