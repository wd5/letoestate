# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from apps.realestate.views import items_loader, show_exclusive_catalog, show_exclusive_item, load_excl_catalog, load_region

from views import index
from faq.views import experts,show_expert
from apps.siteblocks.views import show_reviews, show_parnters

urlpatterns = patterns('',

    (r'^load_items/$',csrf_exempt(items_loader)),
    (r'^load_region/$',csrf_exempt(load_region)),
    url(r'^$',index, name='index'),
    (r'^experts/$', experts),
    (r'^experts/(?P<pk>[^/]+)/$', show_expert),
    (r'^reviews/$', show_reviews),
    (r'^partners/$', show_parnters),
    (r'^exclusive/$', show_exclusive_catalog),
    (r'^exclusive/load_catalog/$', csrf_exempt(load_excl_catalog)),
    (r'^exclusive/(?P<slug>[^/]+)/$',show_exclusive_item),
    (r'^faq/', include('apps.faq.urls')),
    (r'^news/', include('apps.siteblocks.urls')),
    (r'^countries/', include('apps.realestate.urls')),
)


