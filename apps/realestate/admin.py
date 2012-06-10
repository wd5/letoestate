# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor, AdminImageWidget
from models import Country, RE_Region, RRE_Type, CRE_Type, ResidentialRealEstate, CommercialRealEstate, CRE_Attached_photo, RRE_Attached_photo, RRE_AdditionalParameter, CRE_AdditionalParameter, ParameterType
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
    form = CountryAdminForm

class RE_RegionAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'country', 'order', 'is_published',)
    list_display_links = ('id','title', 'country',)
    list_editable = ('order', 'is_published',)
    search_fields = ('title','country',)
    list_filter = ('is_published',)

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
        label = u'Информация о доп. параметрах',
    )
    class Meta:
        model = ResidentialRealEstate

class RR_AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = RRE_Attached_photo

class RR_AddParamInline(AdminImageMixin,admin.TabularInline):
    model = RRE_AdditionalParameter

class ResidentialRealEstateAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('price', 'order', 'is_published',)
    search_fields = ('title', 'description', 'add_parameter_info',)
    list_filter = ('is_published', 'price', 'region', 'rre_type')
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

class CR_AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = CRE_Attached_photo

class CR_AddParamInline(AdminImageMixin,admin.TabularInline):
    model = CRE_AdditionalParameter

class CommercialRealEstateAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'price', 'order', 'is_published',)
    list_display_links = ('id','title', 'slug',)
    list_editable = ('price', 'order', 'is_published',)
    search_fields = ('title', 'description', 'add_parameter_info',)
    list_filter = ('is_published', 'price', 'region', 'cre_type')
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

admin.site.register(Country, CountryAdmin)
admin.site.register(RE_Region, RE_RegionAdmin)
admin.site.register(ParameterType, ParameterTypeAdmin)
admin.site.register(RRE_Type, RRE_TypeAdmin)
admin.site.register(CRE_Type, CRE_TypeAdmin)
admin.site.register(ResidentialRealEstate, ResidentialRealEstateAdmin)
admin.site.register(CommercialRealEstate, CommercialRealEstateAdmin)