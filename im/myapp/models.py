from django.db import models
import datetime, time

class user_base(models.Model):
    type = models.IntegerField(default=0)
    phonenum = models.CharField(max_length=11)
    password = models.CharField(max_length=64)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
    	return 'user_base'

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
    file_id = models.CharField(max_length=100, default='')
    file_type = models.CharField(max_length=10, default='')
    
    def __unicode__(self):
      return 'status'     	
   
    def toJSON(self):
      r = {}
      r['id'] = self.id 
      r['uid'] = self.user.id      
      r['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S") 
      r['text'] = self.text
      r['lat'] = '%f' %self.lat
      r['lng'] = '%f' %self.lng  
      r['num_forward'] = forward.objects.filter(status=self).count()
      r['num_like'] = forward.objects.filter(status=self).count()
      r['num_comment'] = forward.objects.filter(status=self).count()
      r['file_id'] = self.file_id
      r['file_type'] = self.file_type
      
      return r

class comment(models.Model):
    user = models.ForeignKey(user_base)
    status = models.ForeignKey(status)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
    	return 'comment'   

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