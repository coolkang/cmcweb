from django.conf.urls import patterns, url

from relation import views

urlpatterns = patterns('',
    #url(r'^acceptform$', views.acceptform, name='acceptform'),
    url(r'^link$', views.tracklink, name='link'),
    
)


