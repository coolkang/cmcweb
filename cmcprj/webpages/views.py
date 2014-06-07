# -*- coding: utf-8 -*-
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import activate
from cmcprj.settings.base import georeader,BASE_DIR
from django.conf import settings
from models import UserAccess, AccessLocation
import geoip2.database
from geoip2.errors import GeoIP2Error,AddressNotFoundError
import ConfigParser


# set up logging
import logging
logging.basicConfig(filename=os.path.join(BASE_DIR,'LOGS/django.log'),
    level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# URL path dictionary for supported languages (plus country codes).
urlpath_dict = {'en':'en', 'ko':'ko', 'tr':'tr', 'ar':'ar', 'ar-eg':'ar', 
    'zh':'zh', 'zh-cn':'zh'}
lang_choices = [('en',u'English'),('tr',u'Türkçe'),('zh',u'中文'),('ar',u'عربي'),
    ('ko',u'한국어')]


def sendmail(lang, to_mail):
    '''
    It sends a follow up emails to visitors who left their contact info. 
    '''
    
    config = ConfigParser.ConfigParser()
    config_file = 'webpage_%s.cfg' % lang
    path = os.path.join(settings.CONFIGS_DIR, config_file)
    config.read(path)
    subject = config.get('Email', 'subject')
    message = config.get('Email', 'message')
    from_mail = settings.INFO_EMAIL
    recipient_list = [to_mail]
    
    send_mail(subject, message, from_mail, recipient_list, fail_silently=True)


def index(request):
    '''
    Tracks user access and redirect a user to a proper web page.
    '''
    # Determine a url path based on a user's language.
    # First, check if a user selected a specific language code
    
    if 'langcode' in request.GET: 
        lang_code = request.GET['langcode']
    # If no user lang choice, detect a browser language.
    else: 
        lang_code = request.LANGUAGE_CODE    
    request.session.set_expiry(settings.SESSION_EXPIRATION_TIME) 
    if lang_code in urlpath_dict.keys():
        request.session['url_path'] = urlpath_dict[lang_code] 
    else: # Set a default value
        request.session['url_path'] = 'en'
        
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']        
        
    # IP address    
    ip_addr = request.META['REMOTE_ADDR']    
    # Inspect and get a language code from a user's browser
    lang_code = request.LANGUAGE_CODE
    # Create a UserAccess instance to save to db.
    access = UserAccess.create(ip_addr, lang_code, 'na')
    # Recording user access info into database
    access.save()
    # Save geolocation info for the access.
    
    # Create access location information to save
    try:
        geoinfo = georeader.city(access.ip_addr)
        country = geoinfo.country.iso_code 
        city = geoinfo.city.name
        lat = geoinfo.location.latitude
        lon = geoinfo.location.longitude
        location = AccessLocation.create(access_id=access, country=country, 
            city=city, lat=lat, lon=lon)
        location.save()
    except GeoIP2Error as e:
        logger.error(e)
    # To track the user for the next page
    request.session['accessid'] = access.id
    # Get a language choice obj list for user's language choice buttons
    
    return render(request, ('%s/front.html' % request.session['url_path']), 
        {'lang_choices':lang_choices, 'curr_lang':request.session['url_path']})



def message(request):
    # Determine a url path based on a user's language.
    # First, check if a user selected a specific language code
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']
    
    return render(request, ('%s/message.html' % request.session['url_path']), 
        {'lang_choices':lang_choices, 'curr_lang':request.session['url_path']})    



def acceptform(request):
    '''
    Record a user's information who accepted and agreed with a message.
    '''
    # First, check if the current user has come through previous pages.
    # If not, send the user to the front page where a message is.
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']
    # GET method
    if request.method == 'GET':
        '''
        Save if a user accepted the message into UserAccess.
        '''
        accepted = request.GET['accepted']
        accessid = request.session['accessid']
        useraccess = UserAccess.objects.get(id=accessid)
        useraccess.accepted = accepted
        useraccess.save()         
        return render(request, ('%s/acceptform.html' % url_path), 
            {'accepted':accepted, 'mssg':''})
    # POST method
    elif request.method == 'POST':
        email = request.POST['email']
        if 'yes_email' in request.POST: # If the user gave an email.
            if email: # if email is not empty
                # Validate email
                try:
                    validate_email(email)
                except ValidationError:
                    accepted = request.GET['accepted']
                    mssg = 'Invalid email. Please type a valid email.'
                    return render(request, ('%s/acceptform.html' % url_path), 
                        {'accepted':accepted, 'mssg':mssg})   
                # once validated, process submitted information.
                accessid = request.session['accessid']
                useraccess = UserAccess.objects.get(id=accessid)        
                useraccess.email = email
                useraccess.save()
                request.session['has_email'] = True
                # send email
                sendmail(url_path, email)
                
                return redirect('webpages:thanks')     
            else: # if empty email, ask again
                accepted = request.GET['accepted']
                mssg = 'Please type your email.'
                return render(request, ('%s/acceptform.html' % url_path), 
                    {'accepted':accepted, 'mssg':mssg})                
        elif 'no_email' in request.POST: # if the user didn't give an email
            request.session['has_email'] = False
            return redirect('webpages:thanks')
    # Other HTTP methods are not supported.        
    else: 
        return HttpResponseBadRequest # Throw a HTTP 400 error




def thanks(request):
    # First, check if the current user has come through previous pages.
    # If not, send the user to the front page where a message is. 
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']
    has_email = request.session['has_email']
    request.session.clear() # Clear session data
    return render(request,('%s/thanks.html' % url_path),{'has_email':has_email})
    








