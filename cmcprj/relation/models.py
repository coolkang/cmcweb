from django.db import models

# Create your models here.
    
        
class LinkTracking(models.Model):
    '''
    Track of a link use including who clicked which link
    '''
    useraccess = models.ForeignKey('webpages.UserAccess')
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_addr = models.IPAddressField()
    
    @classmethod
    def create(cls, uaid, link, ipa):
        linktracking = cls(useraccess=uaid, link=link, ip_addr=ipa)
        return linktracking
    
    
    
    
    

    
    

    