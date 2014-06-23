from django.shortcuts import render, redirect
from models import LinkTracking
from webpages.models import UserAccess


# Create your views here.

def tracklink(request):
    # Get the rest of the current URL.
    if request.method == 'GET':
        lang_code = request.GET['lang']
        uaid = request.GET['uaid']
        link = request.GET['link']
        ip = request.META['REMOTE_ADDR'] 
        # Get a corresponding useraccess object.
        useraccess = UserAccess.objects.get(pk=uaid)
        if useraccess is None:
            return HttpResponseBadRequest
        tracking = LinkTracking.create(uaid=useraccess, link=link, ipa=ip)
        tracking.save()
        # redirect a user to the link
        return redirect(link)
    else: 
        return HttpResponseBadRequest # Throw a HTTP 400 error