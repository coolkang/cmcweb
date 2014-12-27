from django.conf.urls import patterns, url

from webpages import views

urlpatterns = patterns('',
    url(r'^acceptform$', views.acceptform, name='acceptform'),
    url(r'^thanks$', views.thanks, name='thanks'),
    #url(r'^message$', views.message, name='message'), 
    url(r'^about$', views.about, name='about'), 
    url(r'^$', views.index, name='index'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()