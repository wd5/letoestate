# -*- coding: utf-8 -*-
from apps.faq.models import Expert
from django import template

register = template.Library()

@register.inclusion_tag("faq/block_aid_out.html")
def block_aid_out():
    try:
        experts = Expert.objects.published()
    except Expert.DoesNotExist:
        experts = False
    if experts:
        random = experts.order_by("?")[:1]
        expert = random[0]
    else:
        expert = False
    return {'expert':expert}