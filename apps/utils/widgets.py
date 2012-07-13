# -*- coding: utf-8 -*-
from django import forms
import os
from django.utils.safestring import mark_safe
import settings


class Redactor(forms.Textarea):
    toolbar = u'default' #'mini'
    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/redactor/redactor.js',
            )
        css = {
            'all': ('/media/js/redactor/css/redactor.css',)
        }

    def __init__(self, attrs=None):
        self.attrs = attrs
        if attrs:
            self.attrs.update(attrs)
        super(Redactor,self).__init__(attrs)

    def render(self,name,value,attrs=None):
        rendered = super(Redactor,self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
        $(document).ready(
            function()
            {
                $('#id_%s').redactor({
                    focus: true,
                    toolbar:'%s',
                    imageUpload:'/upload_img/',
                    fileUpload:'/upload_file/',
                    lang:'ru'
                });
            }
        );
        </script>''' % (name,self.toolbar))

class RedactorMini(Redactor):
    toolbar = u'mini'

class RedactorClassic(Redactor):
    toolbar = u'classic'

#class RedactorMicro(Redactor):
#    toolbar = u'micro'


class AdminImageWidget(forms.FileInput):
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append((u'<a target="_blank" href="%s">'
                           u'<img src="%s" style="height: 100px;" /></a>'
                           u'<a href="/admin/crop/%s/?next=/admin/slider/headerslideitem/%s/">Изменить миниатюру</a>'
                           % (value.url, value.url, value.instance.id, value.instance.id)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class LinkWidget(forms.Textarea):
    def render(self,name,value,attrs=None):
        url = value.split('|')
        return mark_safe(u'<a href="%s" target="blank">%s</a>' % (url[1],url[0]))

class AdminImageCrop(forms.FileInput):
    app_and_model = 'shop/category/'
    img_width = 120
    img_height = 120

    def __int__(self, attrs = {}):
        super(AdminImageCrop, self).__init__(attrs)

    def get_url(self, value):
        return u'<a href="/admin/crop/%s%s/?next=/admin/%s%s/">Изменить миниатюру</a>' \
                % (self.app_and_model, value.instance.id, self.app_and_model, value.instance.id)

    def get_img(self, url):
        file, ext = os.path.splitext(url)
        file = u'%s_crop.jpg' % file
        if os.path.isfile( settings.ROOT_PATH +file):
            url_img = file
        else:
            url_img = url
        return u'<img src="%s" style="width: %spx; height: %spx;" />' % (url_img, self.img_width, self.img_height)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append((u'<a target="_blank" href="%s">%s</a>%s' % (value.url, self.get_img(value.url), self.get_url(value))))
        output.append(super(AdminImageCrop, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
