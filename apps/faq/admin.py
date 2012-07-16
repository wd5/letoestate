# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from models import Question,QuestionCategory,Expert
from sorl.thumbnail.admin import AdminImageMixin

class ExpertAdminForm(forms.ModelForm):
    full_description = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 20}),
        label = u'Полное описание',
    )
    class Meta:
        model = Expert

class ExpertAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','full_name', 'is_published','order',)
    list_display_links = ('id','full_name',)
    list_editable = ('is_published','order',)
    search_fields = ('full_name','description',)
    list_filter = ('is_published',)
    form = ExpertAdminForm

class QuestionAdminForm(forms.ModelForm):
    answer = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 20}),
        label = u'Текст',
    )
    class Meta:
        model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','name','email', 'is_published',)
    list_display_links = ('id','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('name','email', 'question', 'answer',)
    list_filter = ('pub_date','is_published',)
    form = QuestionAdminForm

#class QuestionCategoryAdmin(admin.ModelAdmin):
#    list_display = ('title', 'order','is_published',)
#    list_display_links = ('title',)
#    list_editable = ('order','is_published',)

admin.site.register(Expert, ExpertAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(QuestionCategory, QuestionCategoryAdmin)
