from django.http import HttpResponse
from django.shortcuts import render
from models import UserAccess


urlpath_dict = {'en':'en', 'ko':'ko', 'tr':'tr'}


def index(request):
    # Extract user access info
    # Determine a language code that a user uses.
    lang_code = request.LANGUAGE_CODE
    if lang_code in urlpath_dict.keys():
        url_path = urlpath_dict[lang_code]
    else:
        # Set a default value
        url_path = 'en'
    # IP address    
    ip_addr = request.META['REMOTE_ADDR']
    # Create a UserAccess instance to save to db.
    userinfo = UserAccess.create(ip_addr, lang_code, False)
    # Recording user access info into database
    userinfo.save()
    
    # Redirecting a user to their language page.
    #return HttpResponse("request.LANGUAGE_CODE = %s\n" % request.LANGUAGE_CODE)
    return render(request, ('%s/front.html' % url_path), {})

def form_ko(request):
    # TODO: process the submitted form.
    return render(request, ('ko/front.html' % url_path), {})

