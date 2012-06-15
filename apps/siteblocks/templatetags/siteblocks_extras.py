# -*- coding: utf-8 -*-
from apps.siteblocks.models import BottomSiteMenu, Settings, News
from apps.realestate.models import Country
from django import template

register = template.Library()

@register.inclusion_tag("siteblocks/block_menu.html")
def block_menu(url):
    url = url.split('/')

    if url[1]:
        current = u'/%s/' % url[1]
    else:
        current = u'/'

    try:
        if url[2]:
            current = u'/%s/%s/' % (url[1], url[2])
    except:
        pass

    menu = Country.objects.published()
    return {'menu': menu, 'current': current}


@register.inclusion_tag("siteblocks/block_bottom_menu.html")
def block_bottom_menu():
    menu = BottomSiteMenu.objects.published()
    return {'menu': menu}


@register.inclusion_tag("siteblocks/block_news.html")
def block_news_by_country(country_id):
    try:
        if country_id == '':
            news = News.objects.published()[:3]
            curr_country = False
        else:
            try:
                curr_country = Country.objects.get(id=country_id)
            except Country.DoesNotExist:
                curr_country = False
            news = News.objects.filter(country=country_id)[:3]
    except News.DoesNotExist:
        news = False
        curr_country = False
    return {'news': news, 'curr_country': curr_country}

