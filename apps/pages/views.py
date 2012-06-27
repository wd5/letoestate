# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView, DetailView, ListView, RedirectView, View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from apps.pages.models import Page
from apps.siteblocks.models import Settings
import settings

def index(request):
    try:
        page = Page.objects.get(url = 'index')
    except Page.DoesNotExist:
        page = False
    return direct_to_template(request, 'pages/index.html', locals())

def page(request, url):
    if not url.endswith('/'):
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    page = get_object_or_404(Page, url__exact=url)
    return direct_to_template(request, 'pages/default.html', locals())

@csrf_exempt
def static_page(request, template):
    return direct_to_template(request, template, locals())

class SiteMapView(TemplateView):
    template_name = 'pages/site_map.html'

    def get_context_data(self, **kwargs):
        context = super(SiteMapView, self).get_context_data(**kwargs)
        context['pages'] = Page.objects.filter(is_published=True)
        return context

site_map = SiteMapView.as_view()