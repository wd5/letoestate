# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from apps.realestate.views import items_loader, show_exclusive_catalog, show_exclusive_item, load_excl_catalog, load_region

from views import index
from apps.pages.views import site_map
from faq.views import experts,show_expert
from apps.siteblocks.views import show_reviews, show_parnters

from django.contrib.sitemaps import GenericSitemap
from apps.realestate.models import ResidentialRealEstate,CommercialRealEstate,ExclusiveRealEstate
from apps.pages.models import Page

info_dict_pages = {
    'queryset': Page.objects.filter(is_published=True),
}
info_dict_excles = {
    'queryset': ExclusiveRealEstate.objects.published(),
}
info_dict_resides = {
    'queryset': ResidentialRealEstate.objects.published(),
}
info_dict_commerces = {
    'queryset': CommercialRealEstate.objects.published(),
}

sitemaps = {
    'pages': GenericSitemap(info_dict_pages, priority=0.6),
    'exclestate': GenericSitemap(info_dict_excles, priority=0.5),
    'residentialestate': GenericSitemap(info_dict_resides, priority=0.5),
    'commercialestate': GenericSitemap(info_dict_commerces, priority=0.5),
    }


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
    (r'^site_map/', site_map),
    (r'^sitemap.xml$',
     'django.contrib.sitemaps.views.index',
     {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+).xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps})
)


