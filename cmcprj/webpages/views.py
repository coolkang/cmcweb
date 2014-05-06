from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.conf import settings
from models import UserAccess


# URL path dictionary for supported languages (plus country codes).
urlpath_dict = {'en':'en', 'ko':'ko', 'tr':'tr'}


def index(request):
    '''
    Tracks user access and redirect a user to a proper web page.
    '''
    # Determine a url path based on a user's language.
    request.session.set_expiry(settings.SESSION_EXPIRATION_TIME) 
    lang_code = request.LANGUAGE_CODE
    if lang_code in urlpath_dict.keys():
        request.session['url_path'] = urlpath_dict[lang_code] 
    else: # Set a default value
        request.session['url_path'] = 'en'
    # IP address    
    ip_addr = request.META['REMOTE_ADDR']    
    # Inspect and get a language code from a user's browser
    lang_code = request.LANGUAGE_CODE
    # Create a UserAccess instance to save to db.
    access = UserAccess.create(ip_addr, lang_code, 'na')
    # Recording user access info into database
    access.save()
    # To track the user for the next page
    request.session['accessid'] = access.id
    # Save access id into session for tracking
    # Redirecting a user to their language page.
    return render(request, ('%s/front.html' % request.session['url_path']), {})


def acceptform(request):
    '''
    Record a user's information who accepted and agreed with a message.
    '''
    # First, check if the current user has come through previous pages.
    # If not, send the user to the front page where a message is.
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']
    # Save a form info to db.
    if request.method == 'GET':
        '''
        Save if a user accepted the message into UserAccess.
        UserAccess is purely for recording the result of the message acceptance.
        User's email is not stored in UserAccess, and it will be separately 
        saved in UserInfo because of privacy (not to bind IP address and email)
        '''
        accepted = request.GET['accepted']
        accessid = request.session['accessid']
        useraccess = UserAccess.objects.get(id=accessid)
        useraccess.accepted = accepted
        useraccess.save() 
    elif request.method == 'POST':
        accessid = request.session['accessid']
        useraccess = UserAccess.objects.get(id=accessid)        
        useraccess.email = request.POST['email']
        useraccess.save()
        # Go back to the front page with a message
        return redirect('webpages:thanks')
    else: # Other HTTP methods are not supported.
        return HttpResponseBadRequest # Throw a HTTP 400 error
    return render(request, ('%s/acceptform.html' % url_path), 
        {'accepted':accepted})


def thanks(request):
    # First, check if the current user has come through previous pages.
    # If not, send the user to the front page where a message is. 
    if 'url_path' not in request.session:
        return redirect('webpages:index')
    url_path = request.session['url_path']
    print 'expires:',request.session.get_expiry_date()
    request.session.clear() # Clear session data
    return render(request,('%s/thanks.html' % url_path), {})
    
