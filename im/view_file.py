from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_history, file_status
import os
import datetime
import hashlib
from view_auth import GetAuthUserId, AuthException
from view_common import Random_Str, MyHttpResponse


UPLOAD_FILE_PATH = '/var/www/files/'
UPLOAD_BIG_IMAGE_PATH = UPLOAD_FILE_PATH + 'i/b/'
UPLOAD_SMALL_IMAGE_PATH = UPLOAD_FILE_PATH + 'i/s/'
UPLOAD_AUDIO_PATH = UPLOAD_FILE_PATH + 'a/'
SIZE_SMALL_IMAGE = 60

def SaveImage(file):
    ext = ''
    if '.' in file.name:
        ext = file.name.split('.')[-1]
    tmpname = os.path.join(UPLOAD_BIG_IMAGE_PATH, Random_Str(16)) 
    f = open(tmpname, 'w+')
    for chunk in file.chunks():
        f.write(chunk)
    f.seek(0)
    hashname = hashlib.md5(f.read()).hexdigest().upper() + '.' + ext
    filename_b =  os.path.join(UPLOAD_BIG_IMAGE_PATH, hashname) 
    filename_s =  os.path.join(UPLOAD_SMALL_IMAGE_PATH, hashname) 
    os.rename(tmpname, filename_b)  
    os.system('convert %s -resize %d %s' %(filename_b, SIZE_SMALL_IMAGE, filename_s))
    
    url_pic_b = 'http://192.168.77.160/f/i/b/' + hashname
    url_pic_s = 'http://192.168.77.160/f/i/s/' + hashname
    return (url_pic_b, url_pic_s, hashname)
  
def SaveAudio(file):
    ext = ''
    if '.' in file.name:
        ext = file.name.split('.')[-1]
    tmpname = os.path.join(UPLOAD_AUDIO_PATH, Random_Str(16)) 
    f = open(tmpname, 'w+')
    for chunk in file.chunks():
        f.write(chunk)
    f.seek(0)
    hashname = hashlib.md5(f.read()).hexdigest().upper() + '.' + ext
    filename =  os.path.join(UPLOAD_AUDIO_PATH, hashname) 
    os.rename(tmpname, filename)  
    url_audio = 'http://192.168.77.160/f/a/' + hashname
    return url_audio
  

def SaveFile(file):
    ext = ''
    if '.' in file.name:
        ext = file.name.split('.')[-1]
    tmpname = Random_Str(16)
    f = open(os.path.join(UPLOAD_FILE_PATH, tmpname), 'w+')
    for chunk in file.chunks():
        f.write(chunk)
    f.seek(0)
    hashname = hashlib.md5(f.read()).hexdigest().upper()
    filename = hashname + '.' + ext
    os.rename(os.path.join(UPLOAD_FILE_PATH, tmpname), os.path.join(UPLOAD_FILE_PATH, filename))
    f.close()
    return filename   

def UploadFile(request):
    ret = {'retcode': 0, 'info': 'success'}   
  
    try:
        _uid = GetAuthUserId(request)
        _file = request.FILES.get('file')
        #_type = request.FILES.get('type', '')

        fid = SaveFile(_file)
        ret['fid'] = fid
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'auth failed'
    except:
        ret['retcode'] = -1
        ret['info'] = 'UploadFile failed'

    return MyHttpResponse(ret)
    

def DownloadFile(request):
    ret = {'retcode': 0, 'info': 'success'}

    try:
        _uid = GetAuthUserId(request)
        _fid = request.REQUEST.get('fid')
        _type = request.REQUEST.get('type', '')
        _dir = UPLOAD_FILE_PATH
        if _type == 'nearby':
            _dir = UPLOAD_BIG_IMAGE_PATH
            _file_status = file_status.objects.filter(fid=_fid)
            _num = _file_status[0].access_num + 1
            _file_status.update(access_num=_num)

        f = open(os.path.join(_dir, _fid))
        #content_type='application/octet-stream'
        response = HttpResponse(content_type='image/jpg') 
        response['Content-Disposition'] = 'attachment; filename=' +_fid
        response.write(f.read())
        f.close()
        return response
    except AuthException:
        ret['retcode'] = -2
        ret['info'] = 'auth failed'
    except IndexError, IOError:
        ret['retcode'] = -3
        ret['info'] = 'file does not exist'    
    except:
        ret['retcode'] = -1
        ret['info'] = 'download file failed'

    return MyHttpResponse(ret)
