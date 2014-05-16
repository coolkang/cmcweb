from __future__ import absolute_import
from celery import Celery
#from django.conf import settings
from django.core.mail import send_mail
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'cmcprj.settings.local'

app = Celery('cmcprj', backend='amqp', broker='amqp://')

@app.task(bind=True)
def sendmail(self):
    '''
    It sends a follow up emails to visitors who left their contact info. 
    '''
    send_mail('cmcweb email test','Jesus is your savior','hadiye.info@gmail.com',
        ['visiontier@gmail.com'], fail_silently=True)
    
    
    
