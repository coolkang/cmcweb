from django.conf.urls import patterns, url

from webpages import views

urlpatterns = patterns('',
    url(r'^acceptform$', views.acceptform, name='acceptform'),
    url(r'^thanks$', views.thanks, name='thanks'),
    url(r'^$', views.index, name='index'),
)