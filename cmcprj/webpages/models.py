from django.db import models
import uuid


class UserAccess(models.Model):
    ip_addr = models.GenericIPAddressField(max_length=30)
    lang_code = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)
    # accepted value: yes | no | na (not available)
    accepted = models.CharField(max_length=5) 
    email = models.EmailField(null=True, blank=True)    
            
    @classmethod
    def create(cls, ip_addr, lang_code, accepted):
        useraccess = cls(ip_addr=ip_addr, lang_code=lang_code, 
            accepted=accepted)
        return useraccess


class AccessLocation(models.Model):
    access_id = models.OneToOneField(UserAccess)
    country = models.CharField(max_length=50,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    lon = models.FloatField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    @classmethod
    def create(cls, access_id, country, city, lat, lon):
        accesslocation = cls(access_id=access_id,country=country,city=city,
            lat=lat,lon=lon)
        return accesslocation

        
