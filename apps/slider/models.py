# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.utils.utils import ImageField
from apps.utils.managers import PublishedManager

from pytils.translit import translify
from sorl.thumbnail import get_thumbnail

def file_path_Photo(instance, filename):
    return os.path.join('images','slider',  translify(filename).replace(' ', '_') )

class SlideItem(models.Model):
    image = ImageField(verbose_name=u'картинка', upload_to=file_path_Photo)
    title = models.CharField(verbose_name=u'название', max_length=100)
    description = models.TextField(verbose_name=u'описание',)
    url = models.CharField(verbose_name = u'url', max_length = 150,)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'slider_photo')
        verbose_name_plural =_(u'slider_photos')
        ordering = ['-order',]

    def __unicode__(self):
        return u'ID фото %s' %self.id

    def get_absolute_url(self):
        return self.url.strip()

    def admin_photo_preview(self):
        image = self.image
        if image:
            im = get_thumbnail(self.image, '96x96', crop='center', quality=99)
            return u'<span><img src="%s" width="96" height="96"></span>' %im.url
        else:
            return u'<span></span>'
    admin_photo_preview.allow_tags = True
    admin_photo_preview.short_description = u'Превью'

def file_path_headerSlider(instance, filename):
    return os.path.join('images','headerSlider',  translify(filename).replace(' ', '_') )

class HeaderSlideItem(models.Model):
    image = ImageField(verbose_name=u'картинка', upload_to=file_path_headerSlider)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'header_slider')
        verbose_name_plural =_(u'header_sliders')
        ordering = ['-order',]

    def __unicode__(self):
        return u'ID фото %s' %self.id

    def admin_photo_preview(self):
        image = self.image
        if image:
            im = get_thumbnail(self.image, '196x47', crop='center', quality=99)
            return u'<span><img src="%s" width="196" height="47"></span>' %im.url
        else:
            return u'<span></span>'
    admin_photo_preview.allow_tags = True
    admin_photo_preview.short_description = u'Превью'