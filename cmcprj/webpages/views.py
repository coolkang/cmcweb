from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("request.LANGUAGE_CODE = %s\n" % request.LANGUAGE_CODE)
