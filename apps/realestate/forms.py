# -*- coding: utf-8 -*-
from django import forms
from apps.realestate.models import Request

class RequestForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Ф.И.О.'
            }
        ),
        required=True
    )
    contacts = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Контактные данные'
            }
        ),
        required=True
    )
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder':'Примечание'
            }
        ),
        required=False
    )
    url = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )

    class Meta:
        model = Request
        fields = ('name', 'contacts', 'note', 'url',)
