from django.db import models
import datetime, time

class user_base(models.Model):
    type = models.IntegerField(default=0)
    phonenum = models.CharField(max_length=11)
    password = models.CharField(max_length=64)
    created_at = models.DateField(auto_now_add=True)
    default_profile_id = models.IntegerField(default=0)

    def __unicode__(self):
    	return 'user_base'
    	
    def toJSON(self):
      r = {'uid': self.id, 'name': '', 'url_image': '', 'phonenum':self.phonenum}
      if self.default_profile_id > 0:
        _profile = user_profile.objects.get(id=self.default_profile_id)
        r['name'] = _profile.name
        r['url_image'] = _profile.url_image
      return r  
      	  

class user_detail(models.Model):
    user = models.ForeignKey(user_base)
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    birthday = models.DateField()   
    gender = models.CharField(max_length=1)
    province = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    url_avatar = models.CharField(max_length=64)

    def __unicode__(self):
    	return 'user_detail'

class user_profile(models.Model):
    user = models.ForeignKey(user_base)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)   
    age = models.IntegerField(default=1)
    addr = models.CharField(max_length=64)
    category = models.CharField(max_length=64)   
    url_image = models.CharField(max_length=128)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
    	return 'user_profile'

    def toJSON(self):
      r = {}
      r['id'] = self.id 
      r['name'] = self.name
      r['gender'] = self.gender
      r['age'] = self.age
      r['addr'] = self.addr      
      r['category'] = self.category            
      r['url_image'] = self.url_image
      t1 = self.created_at.strftime("%Y-%m-%d %H:%M:%S")  
      t2 = time.mktime(time.strptime(t1, "%Y-%m-%d %H:%M:%S"))
      r['created_at'] =  int(t2)      
      return r

    def toJSONBasic(self):
      r = {}
      r['uid'] = self.user.id 
      r['name'] = self.name
      r['url_image'] = self.url_image
      return r

class user_profile_photowall(models.Model):
    profile = models.ForeignKey(user_profile)
    url_photo_b = models.CharField(max_length=128)
    url_photo_s = models.CharField(max_length=128)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
    	return 'user_profile_photowall'

    def toJSON(self):
      r = {}
      r['id'] = self.id
      r['url_b'] = self.url_photo_b
      r['url_s'] = self.url_photo_s
      t1 = self.created_at.strftime("%Y-%m-%d %H:%M:%S")  
      t2 = time.mktime(time.strptime(t1, "%Y-%m-%d %H:%M:%S"))
      r['created_at'] =  int(t2)      
      return r

class user_online(models.Model):
    user = models.ForeignKey(user_base)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32, blank=True)
    ip_addr = models.IPAddressField(blank=True, default='') 
    lat = models.DecimalField(max_digits=10, decimal_places=4,blank=True,default=0.0)
    lng = models.DecimalField(max_digits=10, decimal_places=4,blank=True,default=0.0)

    def __unicode__(self):
    	return 'user_online'

class user_history(models.Model):
    user = models.ForeignKey(user_base)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)
    ip_addr = models.IPAddressField()
    lat = models.DecimalField(max_digits=10, decimal_places=4)
    lng = models.DecimalField(max_digits=10, decimal_places=4)

    def __unicode__(self):
    	return 'user_history'    	

class status(models.Model):
    user = models.ForeignKey(user_base)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    lat = models.DecimalField(max_digits=10, decimal_places=4)
    lng = models.DecimalField(max_digits=10, decimal_places=4)
    type = models.IntegerField(default=1)
    
    def __unicode__(self):
      return 'status'     	
   
    def toJSON(self):
      r = {}
      r['id'] = self.id 
      r['uid'] = self.user.id
      t1 = self.created_at.strftime("%Y-%m-%d %H:%M:%S")  
      t2 = time.mktime(time.strptime(t1, "%Y-%m-%d %H:%M:%S"))
      r['created_at'] =  int(t2)
      r['type'] = self.type
      r['text'] = self.text
      r['lat'] = '%.5f' %self.lat
      r['lng'] = '%.5f' %self.lng  
      r['num_forward'] = forward.objects.filter(status=self).count()
      r['num_like'] = forward.objects.filter(status=self).count()
      r['num_comment'] = forward.objects.filter(status=self).count()
      if self.type > 1:
        _file =  file_status.objects.get(status=self)
        r = dict(r, **_file.toJSON())
      return r

class file_status(models.Model):
    user = models.ForeignKey(user_base)
    status = models.ForeignKey(status)
    fid = models.CharField(max_length=100)
    access_num = models.IntegerField(default=0)
    file_type = models.CharField(max_length=10, default='')
    url_pic = models.CharField(max_length=100, default='')
    url_pic_tn = models.CharField(max_length=100, default='')
    url_audio = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return 'file_status' 

    def toJSON(self):
        r= {}
        r['fid'] = self.fid
        r['access_num'] = self.access_num
        r['url_pic'] = self.url_pic
        r['url_pic_tn'] = self.url_pic_tn
        #r['url_audio'] = self.url_audio
        #r['file_type'] = self.file_type    
        return r

class comment(models.Model):
    user = models.ForeignKey(user_base)
    status = models.ForeignKey(status)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
    	return 'comment'   

    def toJSON(self):
        r = {}
        r['user'] = self.user.toJSON()
        r['sid'] = self.status.id
        r['text'] = self.text
        t1 = self.created_at.strftime("%Y-%m-%d %H:%M:%S")  
        t2 = time.mktime(time.strptime(t1, "%Y-%m-%d %H:%M:%S"))
        r['created_at'] =  int(t2)        
        return r

class like(models.Model):
    user = models.ForeignKey(user_base)
    status = models.ForeignKey(status)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
    	return 'like'  

class forward(models.Model):
    user = models.ForeignKey(user_base)
    status = models.ForeignKey(status)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
    	return 'forward'

class friends(models.Model):
    user = models.ForeignKey(user_base)
    friend_id = models.BigIntegerField()

    def __unicode__(self):
    	return 'friends'

class fans(models.Model):
    user = models.ForeignKey(user_base)
    fans_id = models.BigIntegerField()

    def __unicode__(self):
    	return 'fans'    	

class account_thirdparty(models.Model):
    user = models.ForeignKey(user_base)
    account_type = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, default='')

    def toJSON(self):
        r = {}
        r['id'] = self.id 
        r['uid'] = self.uid
        r['type'] = self.account_type
        r['access_token'] = self.access_token
        return r