from django.http import HttpResponse
from django.shortcuts import render_to_response
from myapp.models import user_base, user_history, file_status
import os
import datetime
import hashlib
from view_auth import GetAuthUserId, AuthException
from view_common import Random_Str, MyHttpResponse


#ADDR_SERVER = '54.201.119.130/f'
ADDR_SERVER = '192.168.77.160/f'

SIZE_SMALL_IMAGE = 60
UPLOAD_FILE_PATH = '/var/www/files'

MESSAGE_BIG_IMAGE_PATH = UPLOAD_FILE_PATH + '/m/b/'
MESSAGE_SMALL_IMAGE_PATH = UPLOAD_FILE_PATH + '/m/s/'
MESSAGE_AUDIO_PATH = UPLOAD_FILE_PATH + '/m/a/'

STATUS_BIG_IMAGE_PATH = UPLOAD_FILE_PATH + '/s/b/'
STATUS_SMALL_IMAGE_PATH = UPLOAD_FILE_PATH + '/s/s/'
STATUS_AUDIO_PATH = UPLOAD_FILE_PATH + '/s/a/'

PROFILE_IMAGE_PATH = UPLOAD_FILE_PATH + '/p/i/'
PROFILE_BIG_PHOTO_PATH = UPLOAD_FILE_PATH + '/p/p/b/'
PROFILE_SMALL_PHOTO_PATH = UPLOAD_FILE_PATH + '/p/p/s/'

OTHER_PATH = UPLOAD_FILE_PATH + '/o/'

def GetFileExtension(file):
    ext = ''
    if '.' in file.name:
        ext = '.' + file.name.split('.')[-1]
    return ext    

def GetFilePathByType(type):
    if type == 'StatusImage':
        path = [STATUS_BIG_IMAGE_PATH, MESSAGE_SMALL_IMAGE_PATH]
    elif type == 'StatusAudio':
        path = [STATUS_AUDIO_PATH]
    elif type == 'MessageImage':
        path = [MESSAGE_BIG_IMAGE_PATH, MESSAGE_SMALL_IMAGE_PATH]
    elif type == 'MessageAudio':
        path = [MESSAGE_AUDIO_PATH]        
    elif type == 'ProfileImage':
        path = [PROFILE_IMAGE_PATH]
    elif type == 'ProfilePhoto':
        path = [PROFILE_BIG_PHOTO_PATH, PROFILE_SMALL_PHOTO_PATH]
    else:
        path = [OTHER_PATH]
        
    return path
                
def SaveFile(file, type):
    ext = GetFileExtension(file)
    path = GetFilePathByType(type)
    
    content = file.read()
    fid = hashlib.md5(content).hexdigest().upper() + ext
    
    fullpath = os.path.join(path[0], fid)
    f = open(fullpath, 'w+')
    f.write(content)
    f.close()
    
    url1 = 'http://' + ADDR_SERVER + path[0][len(UPLOAD_FILE_PATH):] + fid
    url2 = ''  
    if len(path) > 1:
        os.system('convert %s -resize %d %s' %(fullpath, SIZE_SMALL_IMAGE, os.path.join(path[1], fid)))  
        url2 = 'http://' + ADDR_SERVER + path[1][len(UPLOAD_FILE_PATH):] + fid
    
    return (fid, url1, url2)    
 
def DeleteFile(fid, type):
    _path = GetFilePathByType(type)
    for p in _path:
        _file = os.path.join(p, fid)
        if os.path.isfile(_file):
            try:
                os.remove(_file)
            except:
                pass    
      
def UploadFile(request):
    ret = {'retcode': 0, 'info': 'success'}   
  
    try:
        _uid = GetAuthUserId(request)
        _file = request.FILES.get('file')
        _type = request.REQUEST.get('type', '')

        (fid, url1, url2) = SaveFile(_file, _type)
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
        _nearby = int (request.REQUEST.get('nearby', 0))
        _path = GetFilePathByType(_type)
        f = open(os.path.join(_path[0], _fid))

        if _nearby == 1:
            _file_status = file_status.objects.filter(fid=_fid)
            _num = _file_status[0].access_num + 1
            _file_status.update(access_num=_num)

        if 'Image' in _type or 'Photo' in _type:
            content_type='image/jpg'
        else:
            content_type='application/octet-stream'         
            
        response = HttpResponse(content_type=content_type) 
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
    except :
        ret['retcode'] = -1
        ret['info'] = 'download file failed'

    return MyHttpResponse(ret)
