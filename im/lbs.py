
import time
import json
import requests

ACCESS_KEY_BD = 'a2THEtScvok8jG6IMI7Kn37G'

API_URL_BD = {
    'CreateGeotable' : 'http://api.map.baidu.com/geodata/v3/geotable/create',
    'ListGeotable'   : 'http://api.map.baidu.com/geodata/v3/geotable/list',
    'DetailGeotable' : 'http://api.map.baidu.com/geodata/v3/geotable/detail',
    'UpdateGeotable' : 'http://api.map.baidu.com/geodata/v3/geotable/update',
    'DetailGeotable' : 'http://api.map.baidu.com/geodata/v3/geotable/delete',

    'CreateColumn'   : 'http://api.map.baidu.com/geodata/v3/column/create',
    'ListColumn'     : 'http://api.map.baidu.com/geodata/v3/column/list',
    'DetailColumn'   : 'http://api.map.baidu.com/geodata/v3/column/detail',
    'UpdateColumn'   : 'http://api.map.baidu.com/geodata/v3/column/update',
    'DeleteColumn'   : 'http://api.map.baidu.com/geodata/v3/column/delete',

    'CreatePoi'      : 'http://api.map.baidu.com/geodata/v3/poi/create',
    'ListPoi'        : 'http://api.map.baidu.com/geodata/v3/poi/list',
    'DetailPoi'      : 'http://api.map.baidu.com/geodata/v3/poi/detail',
    'UpdatePoi'      : 'http://api.map.baidu.com/geodata/v3/poi/update',
    'DeletePoi'      : 'http://api.map.baidu.com/geodata/v3/poi/delete',

    'SearchNearby'   : 'http://api.map.baidu.com/geosearch/v3/nearby',

}

ID_GEOTABLE_STATUS = 49452
ID_GEOTABLE_USER = 49769

def CreateGeotable(name):
    para = {
        'name' : name,
        'geotype' : 1,
        'is_published' : 1,
        'ak' : ACCESS_KEY_BD,
    }
    geotable_id = 0
    res = requests.post(API_URL_BD['CreateGeotable'], data=para)
    #print res.content
    res_json = json.loads(res.content)
    if res_json.has_key('status') and res_json['status'] == 0:
        print 'create geotable %s success, id : %d' %(name, res_json['id'])
        return res_json['id']
    else:
        print 'create geotable %s failed' %name
        print res.content    
        return 0   

    print 'init geotable success, geotable_id ', geotable_id

def CreateColumn(geotable_id, name, key, type):
    para = {
        'geotable_id' : geotable_id,
        'name' : name,
        'key'  : key,
        'type' : type,
        'is_sortfilter_field' : 1,
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.post(API_URL_BD['CreateColumn'], data=para)
    res_json = json.loads(res.content)
    if res_json.has_key('status') and res_json['status'] == 0:
        print 'create column %s success' %key
    else:
        print 'create column %s failed' %key
        print res.content

def InitGeotable():
    geotable_id = CreateGeotable('im_status')
    CreateColumn(geotable_id, 'status id', 'sid', 1)
    CreateColumn(geotable_id, 'time_created', 'time_created', 1)
    CreateColumn(geotable_id, 'status type', 'stype', 1)
    
    geotable_id = CreateGeotable('im_user')
    CreateColumn(geotable_id, 'user id', 'userid', 1)

def UploadStatus(sid, lat, lng, type=1):
    para = {
        'geotable_id' : ID_GEOTABLE_STATUS,
        'latitude' : lat,
        'longitude' : lng,
        'coord_type' : 1,
        'sid' : sid,
        'stype': type,
        'time_created' : int(time.time()),
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.post(API_URL_BD['CreatePoi'], data=para)

def QueryStatus(lat, lng, radius=10000, timespan=7200, pagenum=0, type=0):
    result = {
        'total':0,
        'size':0,
        'content':[]
    }

    location = '%f,%f' %(lng, lat)
    ts_now = int(time.time())
    if type > 0:
        filter = 'time_created:%d,%d|stype:%d,%d' %(ts_now-timespan, ts_now, type, type)
    else:
        filter = 'time_created:%d,%d' %(ts_now-timespan, ts_now)

    para = {
        'geotable_id' : ID_GEOTABLE_STATUS,
        'location' : location,
        'radius' : radius,
        'coord_type' : 1,
        'sortby' : 'distance:1|time_created:-1',
        'filter' : filter,
        'page_index': pagenum,
        'q' : '',
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.get(API_URL_BD['SearchNearby'], params=para)
    #print res.content
    res_json = json.loads(res.content)
    if res_json.has_key('status') and res_json['status'] == 0:
        results = res_json['contents']
        result['total'] = res_json['total']
        result['size'] = res_json['size']
        for r in results:
            result['content'].append( (r['sid'], r['distance']) )  
    else:
        print 'Query failed'
        #print res.content

    #print result
    return result    


def UploadUser(uid, lat, lng):
    para = {
        'geotable_id' : ID_GEOTABLE_USER,
        'latitude' : lat,
        'longitude' : lng,
        'coord_type' : 1,
        'userid' : uid,
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.post(API_URL_BD['CreatePoi'], data=para)
    #print res.content

def DeleteUser(uid):
    para = {
        'geotable_id' : ID_GEOTABLE_USER,
        'userid' : uid,
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.post(API_URL_BD['DeletePoi'], data=para)
    #print res.content

def QueryUser(lat, lng, radius=10000, pagenum=0):
    result = {
        'total':0,
        'size':0,
        'content':[]
    }

    location = '%f,%f' %(lng, lat)
    
    para = {
        'geotable_id' : ID_GEOTABLE_USER,
        'location' : location,
        'radius' : radius,
        'coord_type' : 1,
        'sortby' : 'distance:1',
        'page_index': pagenum,
        'q' : '',
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.get(API_URL_BD['SearchNearby'], params=para)
    print res.content
    res_json = json.loads(res.content)
    if res_json.has_key('status') and res_json['status'] == 0:
        results = res_json['contents']
        result['total'] = res_json['total']
        result['size'] = res_json['size']
        for r in results:
            result['content'].append( (r['userid'], r['distance']) )  
    else:
        print 'Query failed'
        #print res.content

    #print result
    return result

def InitData():
    Upload(1, 31.343440009473, 117.59198752882)
    Upload(2, 31.344440009473, 117.59298752882)
    Upload(3, 31.345440009473, 117.59398752882)
    Upload(4, 31.346440009473, 117.59498752882)
    Upload(5, 31.347440009473, 117.59598752882)
    Upload(6, 31.348440009473, 117.59698752882)
    Upload(7, 31.349440009473, 117.59798752882)
    Upload(8, 31.340440009473, 117.59898752882)
    Upload(9, 31.341440009473, 117.59998752882)
    Upload(10, 31.341440009473, 117.59098752882)

if __name__ == "__main__":
    #InitGeotable()
    #UploadUser(100, 31.343440009473, 117.59198752882)
    #DeleteUser(100)
    #QueryUser(31.343440009473, 117.59198752882)
    #InitData()
    #Query(10000, 31.343, 117.591)
    #/geosearch/v3/nearby?ak=a2THEtScvok8jG6IMI7Kn37G&geotable_id=49452&location=117.5469850755,31.352583354522&radius=100000&coord_type=1
    #/geosearch/v3/nearby?radius=100000.0&ak=a2THEtScvok8jG6IMI7Kn37G&geotable_id=49452&location=117.546985%2C31.338963&coord_type=1
    #
    pass
