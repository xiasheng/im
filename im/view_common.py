from django.http import HttpResponse
from random import Random
import json

def Random_Str(randomlength=32):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def MyHttpResponse(ret, statuscode = 0):
    if statuscode != 0:
        _status = statuscode
    elif ret['retcode'] < 0:
        _status = 400
    else:
        _status = 200
    return HttpResponse(json.dumps(ret),  content_type="application/json", status=_status)

