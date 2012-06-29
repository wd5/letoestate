# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor, AdminImageWidget, LinkWidget
from models import Country, RE_Region, RRE_Type, CRE_Type, ExclusiveRealEstate, EXRE_Attached_photo, ResidentialRealEstate, CommercialRealEstate, CRE_Attached_photo, RRE_Attached_photo, RRE_AdditionalParameter, CRE_AdditionalParameter, ParameterType, Request
from sorl.thumbnail.admin import AdminImageMixin

class CountryAdminForm(forms.ModelForm):
    class Meta:
        model = Country

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class CountryAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title', 'slug', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)
    exclude = ('static_page',)
    form = CountryAdminForm

class RE_RegionAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'country', 'order', 'is_published',)
    list_display_links = ('id','title', 'country',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title','country',)
    list_filter = ('is_published','country')

class RRE_TypeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'order', 'is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)

class CRE_TypeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'order', 'is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)

class RREstateAdminForm(forms.ModelForm):
    add_parameter_info = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 20}),
        label = u'Информация о доп. параметрах',required=False
    )
    class Meta:
        model = ResidentialRealEstate

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class RR_AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = RRE_Attached_photo

class RR_AddParamInline(AdminImageMixin,admin.TabularInline):
    model = RRE_AdditionalParameter
    extra = 0

class ResidentialRealEstateAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('price', 'order', 'is_published',)
    search_fields = ('title', 'description', 'add_parameter_info','serial_number',)
    readonly_fields = ('serial_number',)
    list_filter = ('is_published', 'country', 'region', 'rre_type', 'price', )
    form = RREstateAdminForm
    inlines = [
        RR_AttachedPhotoInline,
        RR_AddParamInline,
    ]

class CREstateAdminForm(forms.ModelForm):
    add_parameter_info = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 20}),
        label = u'Информация о доп. параметрах',
    )
    class Meta:
        model = CommercialRealEstate
    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class CR_AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = CRE_Attached_photo

class CR_AddParamInline(AdminImageMixin,admin.TabularInline):
    model = CRE_AdditionalParameter
    extra = 0

class CommercialRealEstateAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('price', 'order', 'is_published',)
    search_fields = ('title', 'description', 'add_parameter_info', 'serial_number',)
    readonly_fields = ('serial_number',)
    list_filter = ('is_published', 'country', 'region', 'cre_type', 'price', )
    form = CREstateAdminForm
    inlines = [
        CR_AttachedPhotoInline,
        CR_AddParamInline,
    ]

class ParameterTypeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'order', 'is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)

class RequestAdminForm(forms.ModelForm):
    url = forms.CharField(
        widget=LinkWidget,
        label = u'Ссылка на объект',
    )
    class Meta:
        model = Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id','date_create','name','a_url',)
    list_display_links =  ('id','date_create','name',)
    search_fields = ('name','contacts', 'note', 'url',)
    form = RequestAdminForm
    list_filter = ('date_create',)

class EXREstateAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 20}),
        label = u'Описание',
    )
    class Meta:
        model = ExclusiveRealEstate

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class EXRE_AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = EXRE_Attached_photo

class ExclusiveRealEstateAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('price', 'order', 'is_published',)
    search_fields = ('title', 'description',)
    list_filter = ('is_published', 'price', 'country')
    form = EXREstateAdminForm
    inlines = [
        EXRE_AttachedPhotoInline,
    ]

admin.site.register(Request, RequestAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(RE_Region, RE_RegionAdmin)
admin.site.register(ParameterType, ParameterTypeAdmin)
admin.site.register(RRE_Type, RRE_TypeAdmin)
admin.site.register(CRE_Type, CRE_TypeAdmin)
admin.site.register(ExclusiveRealEstate, ExclusiveRealEstateAdmin)
admin.site.register(ResidentialRealEstate, ResidentialRealEstateAdmin)
admin.site.register(CommercialRealEstate, CommercialRealEstateAdmin)