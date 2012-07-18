# -*- coding: utf-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django import forms
from apps.siteblocks.models import BottomSiteMenu, Settings, News, Review, Partner
from apps.utils.widgets import Redactor, AdminImageWidget, LinkWidget

class BottomSiteMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_published',)
    list_display_links = ('title', 'url',)
    list_editable = ('order', 'is_published',)

admin.site.register(BottomSiteMenu, BottomSiteMenuAdmin)

#--Виджеты jquery Редактора
class SettingsAdminForm(forms.ModelForm):
    class Meta:
        model = Settings

    def __init__(self, *args, **kwargs):
        super(SettingsAdminForm, self).__init__(*args, **kwargs)
        try:
            instance = kwargs['instance']
        except KeyError:
            instance = False
        if instance:
            if instance.type == u'input':
                self.fields['value'].widget = forms.TextInput()
            elif instance.type == u'textarea':
                self.fields['value'].widget = forms.Textarea()
            elif instance.type == u'redactor':
                self.fields['value'].widget = Redactor(attrs={'cols': 100, 'rows': 10},)

#--Виджеты jquery Редактора

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title','value',)
    fields = ('title','value',)
    form = SettingsAdminForm
admin.site.register(Settings, SettingsAdmin)

class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 30}),
        label = u'Текст',
    )
    class Meta:
        model = News

class NewsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'country', 'date_add', 'is_published',)
    list_display_links = ('title',)
    list_filter = ('is_published', 'date_add', )
    list_editable = ('is_published',)
    form = NewsAdminForm
    date_hierarchy = 'date_add'
admin.site.register(News, NewsAdmin)

class ReviewAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 30}),
        label = u'Текст',
    )
    class Meta:
        model = Review

class ReviewAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title', 'date_add', 'is_published',)
    list_display_links = ('id','title', 'date_add',)
    list_filter = ('is_published', 'date_add', )
    list_editable = ('is_published',)
    form = ReviewAdminForm
admin.site.register(Review, ReviewAdmin)

class ParnterAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget = Redactor(attrs={'cols': 170, 'rows': 30}),
        label = u'Описание',
        required = False,
    )
    class Meta:
        model = Partner

class ParnterAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title', 'url', 'order', 'is_published',)
    list_display_links = ('id','title', 'url',)
    list_filter = ('is_published', )
    list_editable = ('is_published','order',)
    form = ParnterAdminForm
admin.site.register(Partner, ParnterAdmin)

