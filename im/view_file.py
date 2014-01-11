from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_history
import os
import datetime
import hashlib
from view_auth import GetAuthUserId, AuthException
from view_common import Random_Str, MyHttpResponse
   

UPLOAD_FILE_PATH = '/var/www/files/'

def SaveFile(file):
    tmpname = Random_Str(16)
    f = open(os.path.join(UPLOAD_FILE_PATH, tmpname), 'w+')
    for chunk in file.chunks():
        f.write(chunk)
    f.seek(0)
    hashname = hashlib.md5(f.read()).hexdigest().upper()
    os.rename(os.path.join(UPLOAD_FILE_PATH, tmpname), os.path.join(UPLOAD_FILE_PATH, hashname))
    f.close()
    return hashname   

def UploadFile(request):
    ret = {'retcode': 0, 'info': 'success'}   
  
    try:
        _uid = GetAuthUserId(request)
        _file = request.FILES.get('file')
        _type = request.FILES.get('type', '')
        
        fid = SaveFile(_file)
        ret['fid'] = fid
        if _type == 'image':
            ret['fid_s'] = fid  
            ret['fid_m'] = fid
            ret['fid_o'] = fid
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'auth failed'
    except BufferError:
        ret['retcode'] = -1
        ret['info'] = 'UploadFile failed'

    return MyHttpResponse(ret)
    

def DownloadFile(request):
    ret = {'retcode': 0, 'info': 'success'}

    try:
        _uid = GetAuthUserId(request)
        _fid = request.POST.get('fid')
        f = open(os.path.join(UPLOAD_FILE_PATH, _fid))
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' +_fid
        response.write(f.read())
        f.close()
        return response
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'auth failed'
    except:
        ret['retcode'] = -1
        ret['info'] = 'download file failed'

    return MyHttpResponse(ret)