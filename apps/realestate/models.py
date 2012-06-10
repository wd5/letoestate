# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.utils.utils import ImageField
from pytils.translit import translify

from sorl.thumbnail import ImageField as sorl_ImageField
from apps.utils.managers import PublishedManager

def file_path_icons(instance, filename):
    return os.path.join('images','countryIcons',  translify(filename).replace(' ', '_') )

class Country(models.Model):
    title = models.CharField(verbose_name=u'название', max_length=100)
    icon = ImageField(verbose_name=u'картинка', upload_to=file_path_icons)
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице')
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'сountry')
        verbose_name_plural =_(u'сountries')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'countries/%s/' % self.slug

    def get_news(self):
        return self.news_set.published()

    def get_regions(self):
        return self.re_region_set.published()

class RE_Region(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'страна')
    title = models.CharField(verbose_name=u'название', max_length=100)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'region')
        verbose_name_plural =_(u'regions')

    def __unicode__(self):
        return self.title

    def get_rr_estate(self):
        return self.residentialrealestate_set.published()

    def get_cr_estate(self):
        return self.commercialrealestate_set.published()

# ТИПЫ ЖИЛОЙ НЕДВИЖИМОСТИ RRE residential real estate
class RRE_Type(models.Model):
    title = models.CharField(verbose_name=u'название', max_length=100)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'rre_type')
        verbose_name_plural =_(u'rre_types')

    def __unicode__(self):
        return self.title

    def get_estate(self):
        return self.residentialrealestate_set.publihsed()

# ТИПЫ КОММЕРЧЕСКОЙ НЕДВИЖИМОСТИ CRE commercial real estate
class CRE_Type(models.Model):
    title = models.CharField(verbose_name=u'название', max_length=100)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'cre_type')
        verbose_name_plural =_(u'cre_types')

    def __unicode__(self):
        return self.title

    def get_estate(self):
        return self.commercialrealestate_set.publihsed()


def file_path_RE_Images(instance, filename):
    return os.path.join('images','REImages',  translify(filename).replace(' ', '_') )

def str_price(price):
    if not price:
        return u'0'
    value = u'%s' %price
    if price._isinteger():
        value = u'%s' %value[:len(value)-3]
        count = 3
    else:
        count = 6

    if len(value)>count:
        ends = value[len(value)-count:]
        starts = value[:len(value)-count]

        return u'%s %s' %(starts, ends)
    else:
        return value

class ParameterType(models.Model):
    title = models.CharField(verbose_name=u'название', max_length=100)
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'опубликовано', default=True)

    def __unicode__(self):
        return self.title

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'parameter_type')
        verbose_name_plural =_(u'parameter_types')

# жилая недвижимость
class ResidentialRealEstate(models.Model):
    region = models.ForeignKey(RE_Region, verbose_name=u'регион')
    rre_type = models.ForeignKey(RRE_Type, verbose_name=u'тип')
    title = models.CharField(verbose_name=u'название', max_length=255)
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице')
    image = ImageField(verbose_name=u'картинка', upload_to=file_path_RE_Images)
    price = models.DecimalField(verbose_name=u'цена', max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name=u'описание')
    add_parameter_info = models.TextField(verbose_name=u'информация о доп.параметрах')
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order','-region']
        verbose_name =_(u'rr_estate')
        verbose_name_plural =_(u'rr_estates')

    def __unicode__(self):
        return self.title

    def get_src_image(self):
        return self.image.url

    def get_attached_photos(self):
        return self.rre_attached_photo_set.all()

    def get_str_price(self):
        return str_price(self.price)

    def get_parameters(self):
        return self.rre_additionalparameter_set.all()

#    def get_absolute_url(self):
#        return u'%s%s/' % (self.category.get_absolute_url(),self.slug)

class RRE_Attached_photo(models.Model):
    rr_estate = models.ForeignKey(ResidentialRealEstate, verbose_name=u'недвижимость')
    image = ImageField(upload_to=file_path_RE_Images, verbose_name=u'изображение')
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    def __unicode__(self):
        return u'дополнительное изображение №%s' % self.id

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'rre_attached_photo')
        verbose_name_plural = _(u'rre_attached_photos')

    def get_src_image(self):
        return self.image.url

class RRE_AdditionalParameter(models.Model):
    rr_estate = models.ForeignKey(ResidentialRealEstate, verbose_name=u'недвижимость')
    type = models.ForeignKey(ParameterType, verbose_name=u'параметр')
    value = models.DecimalField(verbose_name=u'значение', max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u'%s' % ''

    class Meta:
        verbose_name = _(u'rre_additional_parameter')
        verbose_name_plural = _(u'rre_additional_parameters')

# коммерческая недвижимость
class CommercialRealEstate(models.Model):
    region = models.ForeignKey(RE_Region, verbose_name=u'регион')
    cre_type = models.ForeignKey(CRE_Type, verbose_name=u'тип')
    title = models.CharField(verbose_name=u'название', max_length=255)
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице')
    image = ImageField(verbose_name=u'картинка', upload_to=file_path_RE_Images)
    price = models.DecimalField(verbose_name=u'цена', max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name=u'описание')
    add_parameter_info = models.TextField(verbose_name=u'информация о доп.параметрах')
    order = models.IntegerField(verbose_name=u'порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'cr_estate')
        verbose_name_plural =_(u'cr_estates')

    def __unicode__(self):
        return self.title

    def get_src_image(self):
            return self.image.url

    def get_attached_photos(self):
        return self.cre_attached_photo_set.all()

    def get_str_price(self):
        return str_price(self.price)

    def get_parameters(self):
        return self.cre_additionalparameter_set.all()

#    def get_absolute_url(self):
#        return u'%s%s/' % (self.category.get_absolute_url(),self.slug)

class CRE_Attached_photo(models.Model):
    cr_estate = models.ForeignKey(CommercialRealEstate, verbose_name=u'недвижимость')
    image = ImageField(upload_to=file_path_RE_Images, verbose_name=u'изображение')
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    def __unicode__(self):
        return u'дополнительное изображение №%s' % self.id

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'cre_attached_photo')
        verbose_name_plural = _(u'cre_attached_photos')

    def get_src_image(self):
        return self.image.url

class CRE_AdditionalParameter(models.Model):
    cr_estate = models.ForeignKey(CommercialRealEstate, verbose_name=u'недвижимость')
    type = models.ForeignKey(ParameterType, verbose_name=u'параметр')
    value = models.DecimalField(verbose_name=u'значение', max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u'%s' % ''

    class Meta:
        verbose_name = _(u'cre_additional_parameter')
        verbose_name_plural = _(u'cre_additional_parameters')