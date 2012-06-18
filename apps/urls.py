# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

from views import index
from faq.views import experts

urlpatterns = patterns('',
    url(r'^$',index, name='index'),
    url(r'^experts/$', experts),
    url(r'^faq/', include('apps.faq.urls')),
    url(r'^news/', include('apps.siteblocks.urls')),
    url(r'^countries/', include('apps.realestate.urls')),
)


