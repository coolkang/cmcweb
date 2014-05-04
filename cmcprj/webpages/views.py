from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from models import UserAccess, UserInfo


urlpath_dict = {'en':'en', 'ko':'ko', 'tr':'tr'}


def get_urlpath(request):
    '''
    Helper function to return a proper URL path for each language code.
    '''
    # Check language code in two places
    # TODO
    # 1. lang_code in session that the system created in previous steps.
    # 2. request.LANGUAGE_CODE. If lang_code in session does not exist.
    
    lang_code = request.LANGUAGE_CODE
    
    if lang_code in urlpath_dict.keys():
        url_path = urlpath_dict[lang_code]
    else:
        # Set a default value
        url_path = 'en'
    return url_path    


def index(request):
    '''
    Tracks user access and redirect a user to a proper web page.
    '''
    # Extract user access info
    # Determine a language code that a user uses.
    url_path = get_urlpath(request)
    # IP address    
    ip_addr = request.META['REMOTE_ADDR']
    # Create a UserAccess instance to save to db.
    lang_code = request.LANGUAGE_CODE
    access = UserAccess.create(ip_addr, lang_code, 'na')
    # Recording user access info into database
    access.save()
    # To track the user for the next page
    tk = access.tk
    print tk
    # Save access id into session for tracking
    # Redirecting a user to their language page.
    return render(request, ('%s/front.html' % url_path), {'tk':tk})


def acceptform(request):
    '''
    Record a user's information who accepted and agreed with a message.
    '''
    url_path = get_urlpath(request)
    # Save a form info to db.
    
    if request.method == 'GET':
        '''
        Save if a user accepted the message into UserAccess.
        UserAccess is purely for recording the result of the message acceptance.
        User's email is not stored in UserAccess, and it will be separately 
        saved in UserInfo because of privacy (not to bind IP address and email)
        '''
        accepted = request.GET['accepted']
        tk = request.GET['tk']
        useraccess = UserAccess.objects.get(tk=tk)
        useraccess.accepted = accepted
        useraccess.save() 
    elif request.method == 'POST':
        '''
        If a user want to leave his/her email, the email will be saved in a 
        UserInfo instance. The email will be used to follow up the user with 
        follow-up email.
        '''
        accepted = request.POST['accepted']
        email = request.POST['email']
        userinfo = UserInfo.create(accepted, email)
        userinfo.save()
        # Go back to the front page with a message
        return HttpResponseRedirect('/thanks')
    else:
        pass
    
    return render(request, ('%s/acceptform.html' % url_path), 
        {'accepted':accepted})


def thanks(request):
    url_path = get_urlpath(request)
    return render(request,('%s/thanksform.html' % url_path), {})
    
