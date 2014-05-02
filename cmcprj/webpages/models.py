from django.db import models



class UserAccess(models.Model):
    ip_addr = models.CharField(max_length=30)
    lang_code = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)
    is_yes = models.BooleanField()
    
    @classmethod
    def create(cls, ip_addr, lang_code, is_yes):
        useraccess = cls(ip_addr=ip_addr, lang_code=lang_code, is_yes=is_yes)
        return useraccess
