# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.utils.utils import ImageField
from apps.pages.models import Page
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
    static_page = models.OneToOneField(Page, verbose_name=u'статическая страница', blank=True, null=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'сountry')
        verbose_name_plural =_(u'сountries')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/countries/%s/' % self.slug

    def get_news(self):
        return self.news_set.published()

    def get_regions(self):
        return self.re_region_set.published()

    def get_rre_catalog(self):
        regions = self.get_regions()
        catalog = ResidentialRealEstate.objects.published().select_related().filter(region__in=regions)
        return catalog

    def get_cre_catalog(self):
        regions = self.get_regions()
        catalog = CommercialRealEstate.objects.published().select_related().filter(region__in=regions)
        return catalog

    def get_src_image(self):
        return self.icon.url

    def save(self, force_insert=False, force_update=False, using=None):
        # создаём структуру статических страниц для данной страны:
        if not self.static_page:
            parent_page = Page(title = self.title, url = u'/countries/%s/' % self.slug, parent = None, content = self.title)
            parent_page.save()
            self.static_page = parent_page
            if parent_page:
                child_page1 = Page(title = u'Преимущества покупки недвижимости в %s' % self.title,
                    url = u'/countries/%s/advantage/' % self.slug, parent = parent_page,
                    content = u'Преимущества покупки недвижимости в %s' % self.title)
                child_page1.save()
                child_page2 = Page(title = u'Каталог недвижимости',
                    url = u'/countries/%s/catalog/' % self.slug, parent = parent_page,
                    content = u'Каталог недвижимости')
                child_page2.save()
                child_page3 = Page(title = u'Процедура покупки',
                            url = u'/countries/%s/buy_procedure/' % self.slug, parent = parent_page,
                            content = u'Процедура покупки')
                child_page3.save()
                child_page4 = Page(title = u'Ипотека',
                        url = u'/countries/%s/ipoteca/' % self.slug, parent = parent_page,
                        content = u'Ипотека')
                child_page4.save()
                child_page5 = Page(title = u'Получение вида на жительство',
                    url = u'/countries/%s/residence_permit/' % self.slug, parent = parent_page,
                    content = u'Получение вида на жительство')
                child_page5.save()
                child_page6 = Page(title = u'Расходы на содержание недвижимости',
                    url = u'/countries/%s/maintenance_costs/' % self.slug, parent = parent_page,
                    content = u'Расходы на содержание недвижимости')
                child_page6.save()
                child_page7 = Page(title = u'Новости',
                    url = u'/countries/%s/news/' % self.slug, parent = parent_page,
                    content = u'Новости')
                child_page7.save()
        else:
            parent_page = self.static_page
            parent_page.url = u'/countries/%s/' % self.slug
            parent_page.save()
            child_pages = Page.objects.filter(parent=parent_page)
            for page in child_pages:
                title = page.title
                if title.startswith(u'Преимущества'):
                    page.url = u'/countries/%s/advantage/' % self.slug
                if title.startswith(u'Каталог'):
                    page.url = u'/countries/%s/catalog/' % self.slug
                if title.startswith(u'Процедура'):
                    page.url = u'/countries/%s/buy_procedure/' % self.slug
                if title.startswith(u'Ипотека'):
                    page.url = u'/countries/%s/ipoteca/' % self.slug
                if title.startswith(u'Получение'):
                    page.url = u'/countries/%s/residence_permit/' % self.slug
                if title.startswith(u'Расходы'):
                    page.url = u'/countries/%s/maintenance_costs/' % self.slug
                if title.startswith(u'Новости'):
                    page.url = u'/countries/%s/news/' % self.slug
                page.save()

        if force_insert and force_update:
            raise ValueError("Cannot force both insert and updating in model saving.")
        self.save_base(using=using, force_insert=force_insert, force_update=force_update)

    save.alters_data = True

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

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-order','-region']
        verbose_name =_(u'rr_estate')
        verbose_name_plural =_(u'rr_estates')

    def get_src_image(self):
        return self.image.url

    def get_type_title(self):
        return self.rre_type.title

    def get_attached_photos(self):
        return self.rre_attached_photo_set.all()

    def get_str_price(self):
        return str_price(self.price)

    def get_parameters(self):
        return self.rre_additionalparameter_set.all()

    def get_absolute_url(self):
        return u'%scatalog/residential/%s/' % (self.region.country.get_absolute_url(),self.slug)

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

    def get_str_value(self):
        return str_price(self.value)

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

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-order',]
        verbose_name =_(u'cr_estate')
        verbose_name_plural =_(u'cr_estates')

    def get_src_image(self):
            return self.image.url

    def get_type_title(self):
        return self.cre_type.title

    def get_attached_photos(self):
        return self.cre_attached_photo_set.all()

    def get_str_price(self):
        return str_price(self.price)

    def get_parameters(self):
        return self.cre_additionalparameter_set.all()

    def get_absolute_url(self):
        return u'%scatalog/commertial/%s/' % (self.region.country.get_absolute_url(),self.slug)

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

    def get_str_value(self):
        return str_price(self.value)

class Request(models.Model):
    url = models.CharField(max_length = 255, verbose_name = u'ссылка')
    name = models.CharField(max_length = 150, verbose_name = u'Ф.И.О.')
    contacts = models.CharField(max_length = 255, verbose_name = u'контактные данные')
    note = models.TextField(verbose_name = u'примечание', blank=True)
    date_create = models.DateTimeField(verbose_name = u'дата добавления', default=datetime.now)

    class Meta:
        verbose_name= _(u'request')
        verbose_name_plural = _(u'requests')
        ordering = ['-date_create']

    def __unicode__(self):
        return u'заявка от %s' % self.name

    def a_url(self):
        a_url = self.url
        return u'<a href="%s" target="_blank">%s</a>' % (a_url,a_url)
    a_url.allow_tags = True
    a_url.short_description = u'ссылка на объект'


