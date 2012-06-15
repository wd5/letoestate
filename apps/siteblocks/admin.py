# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.siteblocks.models import BottomSiteMenu, Settings, News

from apps.utils.widgets import RedactorMini,Redactor

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
    list_display = ('title','name','value',)
    form = SettingsAdminForm
admin.site.register(Settings, SettingsAdmin)

class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 30}),
        label = u'Текст',
    )
    class Meta:
        model = News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'date_add', 'is_published',)
    list_display_links = ('title',)
    list_filter = ('is_published', 'date_add', )
    form = NewsAdminForm
    date_hierarchy = 'date_add'

admin.site.register(News, NewsAdmin)

