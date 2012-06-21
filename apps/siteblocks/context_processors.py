# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from apps.slider.models import HeaderSlideItem
from settings import SITE_NAME

def settings(request):
    try:
        contacts = Settings.objects.get(name='tel').value
    except Settings.DoesNotExist:
        contacts = False

    try:
        header_slider = HeaderSlideItem.objects.published()
    except HeaderSlideItem.DoesNotExist:
        header_slider = False

    return {
        'tel': contacts,
        'site_name': SITE_NAME,
        'header_slider': header_slider,
    }