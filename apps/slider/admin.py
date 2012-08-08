# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.slider.models import SlideItem, HeaderSlideItem
from sorl.thumbnail.admin import AdminImageMixin
from apps.utils.widgets import AdminImageCrop, Redactor
from apps.slider.models import HeaderSlideItem
from django import forms

class SliderImage(AdminImageCrop):
    app_and_model = 'slider/headerslideitem/'
    img_width = 1000
    img_height = 300


class SlideItemAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','admin_photo_preview','url','order','is_published',)
    #list_display = ('id','title','url','order','is_published',)
    list_display_links = ('id','title','admin_photo_preview',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)

admin.site.register(SlideItem, SlideItemAdmin)

class SliderAdminForm(forms.ModelForm):
    image = forms.ImageField(widget=SliderImage, label=u'Изображение')
    description = forms.CharField(widget=forms.Textarea(), label = u'Описание',)
    model = HeaderSlideItem

class HeaderSlideItemAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_photo_preview','order','is_published',)
    list_display_links = ('id','admin_photo_preview',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)
    form = SliderAdminForm

admin.site.register(HeaderSlideItem, HeaderSlideItemAdmin)
