# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from apps.siteblocks.models import Settings
from apps.slider.models import SlideItem, HeaderSlideItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from apps.utils.utils import crop_image

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

@login_required()
@csrf_exempt
def slider_crop_image(request, id_image):
    next = request.REQUEST.get('next', None)
    #output_size = [996, 241]
    output_size = [1000, 300]
    if request.method != "POST":
        try:
            image = HeaderSlideItem.objects.get(id=id_image).image
            return direct_to_template(request, 'crop_image.html', locals())
        except HeaderSlideItem.DoesNotExist:
            return HttpResponseRedirect(next)
    else:
        original_img = HeaderSlideItem.objects.get(id=id_image)
        crop_image(request.POST, original_img, output_size)
        return HttpResponseRedirect(next)
