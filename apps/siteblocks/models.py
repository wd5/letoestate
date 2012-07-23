# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
import datetime
import os
from pytils.translit import translify
from django.db.models.signals import post_save
from apps.utils.managers import PublishedManager
from apps.utils.utils import ImageField
from apps.realestate.models import Country

def image_path(self, instance, filename):
    filename = translify(filename).replace(' ', '_')
    return os.path.join('uploads', 'images/menu', filename)

class BottomSiteMenu(models.Model):
    title = models.CharField(max_length = 150, verbose_name = u'название')
    url = models.CharField(verbose_name = u'url', max_length = 150,)
    order = models.IntegerField(verbose_name = u'порядок сортировки', default = 10, help_text = u'чем больше число, тем выше располагается элемент')
    is_published = models.BooleanField(verbose_name=u'опубликовано', default=True,)

    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'menu_item')
        verbose_name_plural =_(u'menu_items')
        ordering = ['-order']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url.strip()

#def strip_url_title(sender, instance, created, **kwargs):
#    # remove the first and the last space
#    instance.title = instance.title.strip()
#    instance.url = instance.url.strip()
#    instance.save()
#
#post_save.connect(strip_url_title, sender=BottomSiteMenu)

type_choices = (
    (u'input',u'input'),
    (u'textarea',u'textarea'),
    (u'redactor',u'redactor'),
)

class Settings(models.Model):
    title = models.CharField(
        verbose_name = u'Название',
        max_length = 150,
    )
    name = models.CharField(
        verbose_name = u'Служебное имя',
        max_length = 250,
    )
    value = models.TextField(
        verbose_name = u'Значение'
    )
    type = models.CharField(
        max_length=20,
        verbose_name=u'Тип значения',
        choices=type_choices
    )
    class Meta:
        verbose_name =_(u'site_setting')
        verbose_name_plural =_(u'site_settings')

    def __unicode__(self):
        return u'%s' % self.name

def file_path_News(instance, filename):
    return os.path.join('images','news',  translify(filename).replace(' ', '_') )

class News(models.Model):
    country = models.ForeignKey(Country,verbose_name = u'страна', null = True, blank=True,)
    title = models.CharField(
        verbose_name = u'Заголовок',
        max_length = 250,
    )
    image = ImageField(
        verbose_name = u'Изображение',
        upload_to = file_path_News,
        blank = True,
    )
    text = models.TextField(
        verbose_name = u'Текст',
    )
    is_published = models.BooleanField(
        verbose_name = u'Опубликовано',
        default = True,
    )
    date_add = models.DateTimeField(
        verbose_name = u'Дата создания',
        default = datetime.datetime.now
    )
    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-date_add', '-id',]
        verbose_name =_(u'news_item')
        verbose_name_plural =_(u'news_items')
        get_latest_by = 'date_add'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/news/%s/' % self.id

def file_path_rewiews(instance, filename):
    return os.path.join('images','reviews',  translify(filename).replace(' ', '_') )

class Review(models.Model):
    image = ImageField(verbose_name=u'картинка', upload_to=file_path_rewiews, blank=True)
    title = models.CharField(verbose_name=u'заголовок', max_length=100)
    text = models.TextField(verbose_name=u'текст')
    date_add = models.DateTimeField(verbose_name = u'дата добавления', default = datetime.datetime.now)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default = True,)

    objects = PublishedManager()

    class Meta:
        ordering = ['-date_add',]
        verbose_name =_(u'review')
        verbose_name_plural =_(u'reviews')
        get_latest_by = 'date_add'

    def __unicode__(self):
        return self.title

    def get_src_image(self):
        return self.image.url

def file_path_partners_logo(instance, filename):
    return os.path.join('images','partnlogos',  translify(filename).replace(' ', '_') )

class Partner(models.Model):
    logo = ImageField(verbose_name=u'картинка', upload_to=file_path_partners_logo, blank=True)
    title = models.CharField(verbose_name=u'название', max_length=100)
    description = models.TextField(verbose_name=u'описание', blank=True)
    url = models.CharField(max_length=100, verbose_name=u'ссылка' #, help_text=u'Адрес страницы,например, "/your_address/"'
    )
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default = True,)

    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'partner')
        verbose_name_plural =_(u'partners')

    def __unicode__(self):
        return self.title

    def get_src_image(self):
        return self.logo.url

class Analytics(models.Model):
    title = models.CharField(
        verbose_name = u'Заголовок',
        max_length = 250,
    )
    short_description = models.CharField(
        max_length = 250,
        verbose_name = u'Краткое описание',
    )
    description = models.TextField(
        verbose_name = u'описание',
    )
    is_published = models.BooleanField(
        verbose_name = u'Опубликовано',
        default = True,
    )
    date_add = models.DateTimeField(
        verbose_name = u'Дата создания',
        default = datetime.datetime.now
    )
    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-date_add', '-id',]
        verbose_name =_(u'analytics_item')
        verbose_name_plural =_(u'analytics_items')
        get_latest_by = 'date_add'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/analytics/%s/' % self.id
