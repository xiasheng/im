
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

ID_GEOTABLE = 49452

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

def InitGeotable(name):
    geotable_id = CreateGeotable(name)
    CreateColumn(geotable_id, 'status id', 'sid', 1)
    CreateColumn(geotable_id, 'time_created', 'time_created', 1)

def Upload(sid, lat, lng):
    para = {
        'geotable_id' : ID_GEOTABLE,
        'latitude' : lat,
        'longitude' : lng,
        'coord_type' : 1,
        'sid' : sid,
        'time_created' : int(time.time()),
        'ak' : ACCESS_KEY_BD,
    }
    res = requests.post(API_URL_BD['CreatePoi'], data=para)

def Query(lat, lng, radius=10000, timespan=7200, pagenum=0):
    result = {
        'total':0,
        'size':0,
        'content':[]
    }
    location = '%f,%f' %(lng, lat)
    ts_now = int(time.time())
    para = {
        'geotable_id' : ID_GEOTABLE,
        'location' : location,
        'radius' : radius,
        'coord_type' : 1,
        'sortby' : 'distance:1|time_created:-1',
        'filter' : 'time_created:%d,%d' %(ts_now-timespan, ts_now),
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
        print res.content

    print result
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
    InitGeotable('im_status')
    #InitData()
    #Query(10000, 31.343, 117.591)
    pass