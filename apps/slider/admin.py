# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.slider.models import SlideItem, HeaderSlideItem
from sorl.thumbnail.admin import AdminImageMixin

class SlideItemAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','admin_photo_preview','url','order','is_published',)
    #list_display = ('id','title','url','order','is_published',)
    list_display_links = ('id','title','admin_photo_preview',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)

admin.site.register(SlideItem, SlideItemAdmin)

class HeaderSlideItemAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_photo_preview','order','is_published',)
    list_display_links = ('id','admin_photo_preview',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)

admin.site.register(HeaderSlideItem, HeaderSlideItemAdmin)