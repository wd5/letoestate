# -*- coding: utf-8 -*-
from apps.pages.models import Page
from django import template

register = template.Library()

@register.inclusion_tag("pages/block_page_summary.html")
def block_page_summary(alias):
    try:
        page = Page.objects.get(url = alias)
        return {'page': page}
    except Page.DoesNotExist:
        return {}

@register.inclusion_tag("pages/left_menu.html")
def get_menu_by_parent(parent, url):
    try:
        url = url.split('/')

        if url[1]:
            current = u'/%s/' % url[1]
        else:
            current = u'/'

        try:
            if url[2]:
                current = u'/%s/%s/' % (url[1], url[2])
                try:
                    if url[3]:
                        current = u'/%s/%s/%s/' % (url[1], url[2], url[3])
                except:
                    pass
        except:
            pass

        child_pages = Page.objects.filter(parent = parent)
        return {'child_pages': child_pages, 'current':current}
    except Page.DoesNotExist:
        return {}
