# -*- coding: utf-8 -*-
import datetime, settings
from django.db.models import Max, Min
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, FormView, DetailView, ListView, RedirectView, View
from apps.realestate.models import Country, ResidentialRealEstate, CRE_Type, CommercialRealEstate, RRE_Type, ParameterType, ExclusiveRealEstate
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
        if item_type == 'residential':
            context['catalog'] = self.object.get_rre_catalog()
            context['estate_types'] = RRE_Type.objects.published()
            item_slug = self.kwargs.get('item', None)
            if item_slug:
                context['catalog_item'] = ResidentialRealEstate.objects.get(slug=item_slug)
        if item_type == 'commertial':
            context['catalog'] = self.object.get_cre_catalog()
            context['estate_types'] = CRE_Type.objects.published()
            item_slug = self.kwargs.get('item', None)
            if item_slug:
                context['catalog_item'] = CommercialRealEstate.objects.get(slug=item_slug)

        dic = context['catalog'].aggregate(Min('price'), Max('price'))
        context['max_price'] = dic['price__max']
        context['min_price'] = dic['price__min']
        try:
            len = context['max_price'] - context['min_price']
            context['step'] = len / 10
        except TypeError:
            context['step'] = False

        try:
            loaded_count = Settings.objects.get(name='loaded_count').value
        except:
            loaded_count = 5
        context['loaded_count'] = int(loaded_count)
        context['catalog'] = context['catalog'][:loaded_count]

        return context

show_residential_catalog = csrf_protect(ShowCatalogView.as_view())
show_commertial_catalog = csrf_protect(ShowCatalogView.as_view())

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
        if type == 'residential':
            try:
                catalog_item = ResidentialRealEstate.objects.get(id=pk)
            except ResidentialRealEstate.DoesNotExist:
                return HttpResponseBadRequest()
        if type == 'commercial':
            try:
                catalog_item = CommercialRealEstate.objects.get(id=pk)
            except ResidentialRealEstate.DoesNotExist:
                return HttpResponseBadRequest()
        if type == 'exclusive':
            try:
                catalog_item = ExclusiveRealEstate.objects.get(id=pk)
            except ResidentialRealEstate.DoesNotExist:
                return HttpResponseBadRequest()

        initial['url'] = u'%s|%s' % (catalog_item.title, catalog_item.get_absolute_url())

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
                url = saved_object.url.split('|')
                message = render_to_string(
                    'realestate/message_template.html',
                        {
                        'saved_object': saved_object,
                        'sitename': settings.SITE_URL,
                        'url_link': url[1],
                        'url_name': url[0]
                    }
                )
                try:
                    emailto = Settings.objects.get(name='workemail').value
                except Settings.DoesNotExist:
                    emailto = False

                if emailto:
                    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
                    msg.content_subtype = "html"
                    msg.send()

                return HttpResponse('success')
            else:
                form_html = render_to_string(
                    'realestate/request_form.html',
                        {'form': form, }
                )
                return HttpResponse(form_html)
        else:
            return HttpResponseBadRequest()

save_request = SaveRequestView.as_view()

class LoadCatalogView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'type' not in request.POST or 'subtype' not in request.POST or 'region' not in request.POST or 'country_id' not in request.POST:
                return HttpResponseBadRequest()

            country_id = request.POST['country_id']
            type = request.POST['type']
            subtype = request.POST['subtype']
            region = request.POST['region']

            try:
                country_id = int(country_id)
            except ValueError:
                return HttpResponseBadRequest()
            if region != "all":
                try:
                    region = int(region)
                except ValueError:
                    return HttpResponseBadRequest()
            if subtype != "all":
                try:
                    subtype = int(subtype)
                except ValueError:
                    return HttpResponseBadRequest()
            if subtype != 'all' and region != 'all':
                condition = u'get_estate().filter(region=%s)' % region
            else:
                condition = False

            if type == "residential":
                country = Country.objects.get(pk=country_id)
                queryset = country.get_rre_catalog()

                #queryset = ResidentialRealEstate.objects.published().filter()

                if subtype == "all":
                    if region == "all":
                        pass
                    else:
                        queryset = queryset.filter(region=region)
                else:
                    if region == "all":
                        queryset = queryset.filter(rre_type=subtype)
                    else:
                        queryset = queryset.filter(rre_type=subtype).filter(region=region)
            elif type == "commertial":
                country = Country.objects.get(pk=country_id)
                queryset = country.get_cre_catalog()

                #queryset = CommercialRealEstate.objects.published().filter()
                if subtype == "all":
                    if region == "all":
                        pass
                    else:
                        queryset = queryset.filter(region=region)
                else:
                    if region == "all":
                        queryset = queryset.filter(cre_type=subtype)
                    else:
                        queryset = queryset.filter(cre_type=subtype).filter(region=region)
            else:
                return HttpResponseBadRequest('Произошла ошибка. Приносим извинения.')

            dic = queryset.aggregate(Min('price'), Max('price'))
            max_price = dic['price__max']
            min_price = dic['price__min']
            try:
                len = max_price - min_price
                step = len / 10
            except TypeError:
                step = False

            try:
                loaded_count = Settings.objects.get(name='loaded_count').value
            except:
                loaded_count = 5
            loaded_count = int(loaded_count)

            items_html = render_to_string(
                'realestate/catalog_template.html',
                    {'catalog': queryset[:loaded_count], 'loaded_count': loaded_count, 'request': request,
                     'type': type, 'region': region, 'subtype': subtype, 'country_id': country_id,
                     'condition': condition,
                     'max_price': max_price, 'min_price': min_price, 'step': step}
            )
            return HttpResponse(items_html)
        else:
            return HttpResponseBadRequest()

load_catalog = LoadCatalogView.as_view()

class ExclusiveCatalogView(ListView):
    model = ExclusiveRealEstate
    template_name = 'realestate/exclusive_catalog.html'
    context_object_name = 'catalog'
    queryset = model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(ExclusiveCatalogView, self).get_context_data(**kwargs)
        item = self.kwargs.get('slug', None)

        dic = context['catalog'].aggregate(Min('price'), Max('price'))
        context['max_price'] = dic['price__max']
        context['min_price'] = dic['price__min']
        try:
            len = context['max_price'] - context['min_price']
            context['step'] = len / 10
        except TypeError:
            context['step'] = False

        try:
            loaded_count = Settings.objects.get(name='loaded_count').value
        except:
            loaded_count = 5
        context['loaded_count'] = int(loaded_count)
        context['countries'] = ExclusiveRealEstate.objects.values('country').distinct().order_by('country')
        context['catalog'] = context['catalog'][:loaded_count]
        return context

show_exclusive_catalog = ExclusiveCatalogView.as_view()

class ShowExclusiveItemView(DetailView):
    slug_field = 'slug'
    model = ExclusiveRealEstate
    template_name = 'realestate/show_exclusive_item.html'
    context_object_name = 'item'

show_exclusive_item = ShowExclusiveItemView.as_view()

class LoadExclCatalogView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'country' not in request.POST:
                return HttpResponseBadRequest()
            country = request.POST['country']
            try:
                loaded_count = Settings.objects.get(name='loaded_count').value
            except:
                loaded_count = 5
            loaded_count = int(loaded_count)

            if country == "all":
                queryset = ExclusiveRealEstate.objects.published()[:loaded_count]
                condition = ''
            else:
                queryset = ExclusiveRealEstate.objects.filter(country=country)[:loaded_count]
                condition = 'filter(country="%s")' % country

            dic = queryset.aggregate(Min('price'), Max('price'))
            max_price = dic['price__max']
            min_price = dic['price__min']
            try:
                len = max_price - min_price
                step = len / 10
            except TypeError:
                step = False

            try:
                loaded_count = Settings.objects.get(name='loaded_count').value
            except:
                loaded_count = 5
            loaded_count = int(loaded_count)

            items_html = render_to_string(
                'realestate/excl_catalog_template.html',
                    {'catalog': queryset[:loaded_count], 'loaded_count': loaded_count, 'request': request,
                     'condition': condition,
                     'country': country, 'max_price': max_price, 'min_price': min_price, 'step': step}
            )
            return HttpResponse(items_html)
        else:
            return HttpResponseBadRequest()

load_excl_catalog = LoadExclCatalogView.as_view()

class LoadRegionAdmin(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'id_country' not in request.POST:
                return HttpResponseBadRequest()

            id_country = request.POST['id_country']

            try:
                id_country = int(id_country)
            except ValueError:
                return HttpResponseBadRequest()

            try:
                curr_country = Country.objects.get(id=id_country)
            except Country.DoesNotExist:
                return HttpResponseBadRequest()

            regions = curr_country.get_regions()
            html_code = u'<option value=""></option>'
            for region in regions:
                html_code = u'%s<option value="%s">%s</option>' % (html_code,region.id,region.title)
            return HttpResponse(html_code)
        else:
            return HttpResponseBadRequest()

load_region = LoadRegionAdmin.as_view()