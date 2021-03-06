# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from apps.realestate.views import show_residential_catalog,show_commercial_catalog, show_country, show_news, news_detail, show_catalog_item, send_request, save_request, load_catalog
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',

    (r'^$',show_country,{'pk':'1'}),
    (r'^load_catalog/$',csrf_exempt(load_catalog)),
    (r'^send_request/(?P<type>[^/]+)/(?P<pk>\d*)/$',send_request),
    (r'^save_request/$',csrf_exempt(save_request)),
    (r'^catalog/catalog/$', lambda x:HttpResponseRedirect('/')),
    (r'^(?P<slug>[^/]+)/$',show_country),
    (r'^(?P<slug>[^/]+)/catalog/$',show_residential_catalog),
    (r'^(?P<slug>[^/]+)/catalog/(?P<type>[^/]+)/$',show_residential_catalog),
    (r'^(?P<slug>[^/]+)/catalog/(?P<type>[^/]+)/$',show_commercial_catalog),
    (r'^(?P<slug>[^/]+)/catalog/(?P<type>[^/]+)/(?P<item>[^/]+)/$',show_catalog_item),
    (r'^(?P<slug>[^/]+)/catalog/(?P<type>[^/]+)/(?P<item>[^/]+)/$',show_catalog_item),
    (r'^(?P<slug>[^/]+)/news/$',show_news),
    (r'^(?P<slug>[^/]+)/news/$',show_news),
    (r'^(?P<slug>[^/]+)/news/(?P<pk>\d*)/$', news_detail),


)
