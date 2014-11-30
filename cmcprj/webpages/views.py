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
import codecs


# set up logging
import logging
logging.basicConfig(filename=os.path.join(BASE_DIR,'LOGS/django.log'),
    level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# URL path dictionary for supported languages (plus country codes).
urlpath_dict = {'en':'en', 'tr':'tr', 'ar':'ar', 'ar-eg':'ar', 'ar-dz':'ar',
    'ar-bh':'ar', 'ar-iq':'ar', 'ar-jo':'ar', 'ar-kw':'ar', 'ar-lb':'ar',
    'ar-ly':'ar', 'ar-ma':'ar', 'ar-om':'ar', 'ar-qa':'ar', 'ar-sa':'ar',
    'ar-sy':'ar', 'ar-tn':'ar', 'ar-ae':'ar', 'zh':'zh', 'zh-cn':'zh', 
    'ru':'ru', 'ru-mo':'ru'}
    
lang_choices = [('en',u'English'),('tr',u'Türkçe'),('zh',u'中文'),('ar',u'عربي'),('ru',u'русский')]


# Additional content in a follow-up email.
zh = ['http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_410-jf-0-0_1343780049-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201305/1690/1226740748001_2418283993001_My-Last-Day-Uyghur-1-1-80856.mp4',
        'http://brightcove04.brightcove.com/29/1226740748001/83/GSFN_529-0-La_Busqueda_The_Search_1351531803-MP4-320-240-150000.mp4']
        
tr = ['http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_1942-jf-0-0_1343442320-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201401/1593/1226740748001_3105942491001_Magdalena--60-min--Turkish-1-1-87055.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201405/2644/1226740748001_3597062364001_Prize3-Turkish-720.mp4',
        'http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_1942-cl-0-0_1343442379-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_1942-mld-0-0_1343442390-MP4-320-240-150000.mp4'] 

ar = ['http://brightcove04.brightcove.com/29/1226740748001/971/WESS_53441-jf-0-0_1349446508-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201312/2696/1226740748001_2930096866001_Magdalena--60-min--Arabic--Modern-Standard--Egyptian--1-1-86983.mp4',
        'http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_22658-mld-0-0_1343442396-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_22658-cl-0-0_1343442349-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201405/1616/1226740748001_3577767019001_Prize3-Arabic-720.mp4']

en = ['http://brightcove04.brightcove.com/29/1226740748001/s1/WESS_529-jf-0-0_1343439914-MP4-320-240-150000.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201401/1769/1226740748001_3105866259001_Magdalena--60-min--English-1-1-87069.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/136/1226740748001_2241999675001_7DWJGrace-1-7-English.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/3136/1226740748001_2241999716001_7DWJGrace-2-7-English.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/3136/1226740748001_2241999671001_7DWJGrace-3-7-English.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/136/1226740748001_2241999683001_7DWJGrace-4-7-English.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/1136/1226740748001_2241999673001_7DWJGrace-5-7-English.mp4',
        'http://brightcove04.brightcove.com/21/1226740748001/201303/1136/1226740748001_2241999686001_7DWJGrace-6-7-English.mp4',
        'http://aa997190d22ac202e45b-00ed99dd1fad6f1ae9b61d4c75fe96ca.r10.cf1.rackcdn.com/GraceDay07cinematic640x300.jpg',
        ]

ru = ['http://jesusfilmmedia.org/video/1_3934-jf-0-0', 
        'http://jesusfilmmedia.org/video/1_3934-wl60-0-0']

links_dict = {'zh':zh, 'tr':tr, 'ar':ar, 'en':en, 'ru':ru}



def sendmail(lang, to_mail, accessid):
    '''
    It sends a follow up emails to visitors who left their contact info. 
    '''
    
    config = ConfigParser.ConfigParser()
    config_file = 'webpage_%s.cfg' % lang
    path = os.path.join(settings.CONFIGS_DIR, config_file)
    
    # TODO: improve this part.
    if lang == 'ar':
        subject = r'محبة الله'
        message = r'''شكرا لزيارتك موقعنا www.hadiye.org.
إذا كان لديك أي سؤال، وارسل البريد الإلكتروني إلى info@hadiye.org.
وسوف نرسل لك المزيد من المحتويات التي قد تساعدك على النحو التالي؛
شكرا.
'''
    else:
        #config.read(path)
        config.readfp(codecs.open(path, 'r','utf8'))
        subject = config.get('Email', 'subject')
        message = config.get('Email', 'message')
        
    url_str = "http://hadiye.org/relation/link?uaid=%s&lang=%s&link=%s"
        
    links = links_dict[lang]
    for link in links:
        str = url_str % (accessid, lang, link)
        message = message + '\n\n' + str
             
        
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
    
    return render(request, ('%s/message.html' % request.session['url_path']), 
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
        request.session['accepted'] = accepted     
        print 'in session, accepted', request.session['accepted']    
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
                sendmail(url_path, email, accessid)
                
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
    accepted = request.session['accepted']
    request.session.clear() # Clear session data
    return render(request,('%s/thanks.html' % url_path),{'has_email':has_email, 
        'accepted':accepted})
    








