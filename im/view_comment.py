from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, status, comment, like
from view_auth import GetAuthUserId, AuthException
from view_common import MyHttpResponse

def AddComment(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _sid = request.REQUEST.get('sid')
        _text = request.REQUEST.get('text')

        _user = user_base(id=_uid)
        _status = status(id=_sid)

        _comment = comment(user=_user, status=_status, text=_text)
        _comment.save()
        ret['id'] = _comment.id
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'AddComment failed'          

    return MyHttpResponse(ret) 

def DelCommentById(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _id = request.REQUEST.get('id')

        _user = user_base(id=_uid)

        comment.objects.get(user=_user, id=_id).delete()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'DelCommentById failed'          

    return MyHttpResponse(ret)


def GetCommentById(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _id = request.REQUEST.get('id')
        _comment = comment.objects.get(id=_id)

        ret['comment'] = _comment.toJSON()
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'GetCommentById failed'          

    return MyHttpResponse(ret)

def BatchGetCommentByIds(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _ids = request.REQUEST.get('ids', []).split(',') 
        _comments = comment.objects.filter(pk__in=_ids)

        _list__comments = []
        for c in _comments:
            _list__comments.append(c.toJSON())
              
        ret['comments'] = _list__comments
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except:
        ret['retcode'] = -1
        ret['info'] = 'BatchGetCommentByIds failed'          

    return MyHttpResponse(ret)

def GetCommentListByStatusId(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        _sid = request.REQUEST.get('sid')
        _status = status(id=_sid)

        _comment_list = comment.objects.filter(status=_status)
        _ids = []
        for c in _comment_list:
            _ids.append(c.id)

        ret['ids'] = _ids
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except IOError:
        ret['retcode'] = -1
        ret['info'] = 'GetCommentListByStatusId failed'          

    return MyHttpResponse(ret)

def GetCommentDetailByStatusId(request):
    ret = {'retcode': 0, 'info': 'success', 'hasmore': 0}
    try:
        _uid = GetAuthUserId(request)
        _sid = request.REQUEST.get('sid')
        _pagenum = request.REQUEST.get('pagenum', 0)
        _pagenum = int(_pagenum)

        _status = status(id=_sid)

        _total = comment.objects.filter(status=_status).count()
        _comments = comment.objects.filter(status=_status).order_by('-id')[_pagenum*10:(_pagenum+1)*10]
        _comments_list = []
        for c in _comments:
            _comments_list.append(c.toJSON())

        ret['comments'] = _comments_list
        ret['total'] = _total
        ret['pagenum'] = _pagenum
        ret['size'] = len(_comments)
        if _total/10 > _pagenum:
            ret['hasmore'] = 1
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except IOError:
        ret['retcode'] = -1
        ret['info'] = 'GetCommentListByStatusId failed'          

    return MyHttpResponse(ret)

def AddLike(request):
    ret = {'retcode': 0, 'info': 'success'}
    try:
        _uid = GetAuthUserId(request)
        
        _sid = request.REQUEST.get('sid')

        _user = user_base(id=_uid)
        _status = status(id=_sid)

        _like = like(user=_user, status=_status)
        _like.save()
        ret['id'] = _like.id
         
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'unauthorized'
    except :
        ret['retcode'] = -1
        ret['info'] = 'AddLike failed'          

    return MyHttpResponse(ret)     