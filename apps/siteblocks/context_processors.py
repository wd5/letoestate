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
        email = Settings.objects.get(name='workemail').value
    except Settings.DoesNotExist:
        email = False

    try:
        header_slider = HeaderSlideItem.objects.published()
    except HeaderSlideItem.DoesNotExist:
        header_slider = False

    return {
        'tel': contacts,
        'email': email,
        'site_name': SITE_NAME,
        'header_slider': header_slider,
    }