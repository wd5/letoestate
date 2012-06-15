# -*- coding: utf-8 -*-
import datetime, settings
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView, DetailView, ListView, RedirectView, View
from apps.realestate.models import Country, ResidentialRealEstate, CRE_Type, CommercialRealEstate, RRE_Type, ParameterType
from apps.siteblocks.models import News, Settings
from apps.realestate.forms import RequestForm
from django.core.mail.message import EmailMessage

class ShowCatalogView(DetailView):
    model = Country
    template_name = 'realestate/show_catalog.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ShowCatalogView, self).get_context_data(**kwargs)
        # Residential
        context['regions'] = self.object.get_regions()
        context['additional_parameters'] = ParameterType.objects.published()
        item_type = self.kwargs.get('type', 'residential')
        context['item_type'] = item_type
        if item_type=='residential':
            context['catalog'] = self.object.get_rre_catalog()
            context['estate_types'] = RRE_Type.objects.published()
            item_slug = self.kwargs.get('item', None)
            if item_slug:
                context['catalog_item'] = ResidentialRealEstate.objects.get(slug=item_slug)
        if item_type=='commertial':
            context['catalog'] = self.object.get_cre_catalog()
            context['estate_types'] = CRE_Type.objects.published()
            item_slug = self.kwargs.get('item', None)
            if item_slug:
                context['catalog_item'] = CommercialRealEstate.objects.get(slug=item_slug)
        return context

show_residential_catalog = ShowCatalogView.as_view()
show_commertial_catalog = ShowCatalogView.as_view()

class ShowCatalogItemView(DetailView):
    model = Country
    template_name = 'realestate/show_catalog_item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ShowCatalogItemView, self).get_context_data(**kwargs)
        item_slug = self.kwargs.get('item', None)
        item_type = self.kwargs.get('type', None)
        if item_slug and item_type:
            if item_type == 'residential':
                model = ResidentialRealEstate
            if item_type == 'commertial':
                model = CommercialRealEstate
            context['item_type'] = item_type
            try:
                context['catalog_item'] = model.objects.get(slug=item_slug)
            except model.DoesNotExist:
                pass
        return context

show_catalog_item = ShowCatalogItemView.as_view()

class ShowNewsView(DetailView):
    model = Country
    template_name = 'siteblocks/news_list.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ShowNewsView, self).get_context_data(**kwargs)
        context['news'] = self.object.get_news()
        new_pk = self.kwargs.get('pk', None)
        if new_pk:
            self.template_name = 'siteblocks/new_detail.html'
            context['news_current'] = News.objects.get(pk=new_pk)
        return context

show_news = ShowNewsView.as_view()

class ShowDetailNewView(DetailView):
    model = News
    slug_field = 'pk'
    template_name = 'siteblocks/new_detail.html'
    context_object_name = 'news_current'

    def get_context_data(self, **kwargs):
        context = super(ShowDetailNewView, self).get_context_data(**kwargs)
        item = self.kwargs.get('slug', None)
        if item:
            context['item'] = Country.objects.get(slug=item)
        return context

news_detail = ShowDetailNewView.as_view()

class ShowCountryView(RedirectView):
    url = 'advantage/'

show_country = ShowCountryView.as_view()

class RequestFormView(FormView):
    form_class = RequestForm
    template_name = 'realestate/request_form.html'

    def get_form_kwargs(self):
        kwargs = super(RequestFormView, self).get_form_kwargs()
        initial = self.get_initial()

        try:
            pk = self.kwargs['pk']
            type = self.kwargs['type']
        except KeyError:
            return HttpResponseBadRequest()
        if type=='residential':
            try:
                catalog_item = ResidentialRealEstate.objects.get(id=pk)
            except ResidentialRealEstate.DoesNotExist:
                return HttpResponseBadRequest()
        if type=='commercial':
            try:
                catalog_item = CommercialRealEstate.objects.get(id=pk)
            except ResidentialRealEstate.DoesNotExist:
                return HttpResponseBadRequest()

        initial['url'] = catalog_item.get_absolute_url()

        kwargs.update({
            'initial': initial,
        })
        return kwargs

send_request = RequestFormView.as_view()

class SaveRequestView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST.copy()
            form = RequestForm(data)
            if form.is_valid():
                saved_object = form.save()
                subject = u'LetoEstate - Информация о заявке.'
                subject = u''.join(subject.splitlines())
                message = render_to_string(
                    'realestate/message_template.html',
                    {
                        'saved_object':saved_object,
                    }
                )
                try:
                    emailto = Settings.objects.get(name='workemail').value
                except Settings.DoesNotExist:
                    emailto = False

                if emailto:
                    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,[emailto])
                    msg.content_subtype = "html"
                    msg.send()

                return HttpResponse('success')
            else:
                form_html = render_to_string(
                    'realestate/request_form.html',
                        {'form': form,}
                )
                return HttpResponse(form_html)

save_request = SaveRequestView.as_view()
