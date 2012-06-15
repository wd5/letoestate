# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from apps.siteblocks.models import Settings
from apps.slider.models import SlideItem


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        try:
            specs = SlideItem.objects.published()
        except SlideItem.DoesNotExist:
            specs = False
        context['specs'] = specs
        try:
            main_text = Settings.objects.get(name='main_text').value
        except Settings.DoesNotExist:
            main_text = ''
        context['main_text'] = main_text
        try:
            description_text = Settings.objects.get(name='description_text').value
        except Settings.DoesNotExist:
            description_text = ''
        context['description_text'] = description_text
        try:
            seo_text = Settings.objects.get(name='seo_text').value
        except Settings.DoesNotExist:
            seo_text = ''
        context['seo_text'] = seo_text

        return context

index = IndexView.as_view()