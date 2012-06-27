# -*- coding: utf-8 -*-
import datetime, settings
from django.db.models import Max, Min
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, FormView, DetailView, ListView, RedirectView, View
from django.db.models.loading import get_model
from apps.realestate.models import Country, ResidentialRealEstate, CRE_Type, CommercialRealEstate, RRE_Type, ParameterType, ExclusiveRealEstate
from apps.siteblocks.models import News, Settings
from apps.realestate.forms import RequestForm
from django.core.mail.message import EmailMessage

def GetLoadIds(queryset, loaded_count):
    counter = 0
    next_id_loaded_items = ''
    for item in queryset[loaded_count:]:
        counter = counter + 1
        div = counter % loaded_count
        next_id_loaded_items = u'%s,%s' % (next_id_loaded_items, item.id)
        if div == 0:
            next_id_loaded_items = u'%s|' % next_id_loaded_items

    if next_id_loaded_items.startswith(',') or next_id_loaded_items.startswith('|'):
        next_id_loaded_items = next_id_loaded_items[1:]
    if next_id_loaded_items.endswith(',') or next_id_loaded_items.endswith('|'):
        next_id_loaded_items = next_id_loaded_items[:-1]
    next_id_loaded_items = next_id_loaded_items.replace('|,', '|')

    next_block_ids = next_id_loaded_items.split('|')[0]
    if next_block_ids != '':
        next_block_ids = next_block_ids.split(',')
        next_block_ids = len(next_block_ids)
        if loaded_count > next_block_ids:
            loaded_count = next_block_ids
    else:
        loaded_count = False

    result = u'%s!%s' % (loaded_count, next_id_loaded_items)
    return result


class ShowCatalogView(DetailView):
    model = Country
    template_name = 'realestate/show_catalog.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ShowCatalogView, self).get_context_data(**kwargs)
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
            loaded_count = int(Settings.objects.get(name='loaded_count').value)
        except:
            loaded_count = 5
        queryset = context['catalog']
        result = GetLoadIds(queryset, loaded_count)
        splited_result = result.split('!')
        try:
            remaining_count = int(splited_result[0])
        except:
            remaining_count = False
        next_id_loaded_items = splited_result[1]

        parameters = ''
        for item in context['additional_parameters']:
            value_max = 0
            value_min = 10000000
            for estate in context['catalog']:
                estate_parameters_set = estate.get_parameters()
                if estate_parameters_set:
                    try:
                        curr_param_value = estate_parameters_set.get(type=item.id).value
                        if curr_param_value > value_max:
                            value_max = curr_param_value
                        if curr_param_value < value_min and curr_param_value != 0:
                            value_min = curr_param_value
                    except:
                        pass
            if value_min==10000000: value_min = 0
            item.max_val=value_max
            item.min_val=value_min
            if value_max==value_min or value_max<value_min:
                disabled=True
                item.slider_disable='true'
                item.max_val=1
                item.min_val=0
                item.step=1
            elif value_max>value_min:
                disabled=False
                add_p_len = value_max - value_min
                add_p_step = add_p_len / 10
                if add_p_step<1:
                    add_p_step=1
                item.step=round(add_p_step)
                item.slider_disable='false'
            parameters = u'%s%s,%s,%s,%s|' % (parameters, item.id, value_min, value_max, disabled)

        if parameters.startswith(',') or parameters.startswith('|'):
            parameters = parameters[1:]
        if parameters.endswith(',') or parameters.endswith('|'):
            parameters = parameters[:-1]
        parameters = parameters.replace('|,', '|')


        context['additional_parameters_string'] = parameters
        context['loaded_count'] = remaining_count
        context['catalog'] = context['catalog'][:loaded_count]
        context['next_id_loaded_items'] = next_id_loaded_items
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

            if 'price_min' in request.POST and 'price_max' in request.POST:
                try:
                    price_min = int(request.POST['price_min'])
                    price_max = int(request.POST['price_max'])
                except:
                    return HttpResponseBadRequest()
            else:
                price_min = False
                price_max = False

            if 'add_parameters_values' in request.POST:
                try:
                    add_parameters_values = request.POST['add_parameters_values']
                except:
                    return HttpResponseBadRequest()
            else:
                add_parameters_values = False

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

            if price_min and price_max:
                queryset = queryset.filter(price__gte=price_min)
                queryset = queryset.filter(price__lte=price_max)

            if add_parameters_values:
                for item in add_parameters_values.split('|'):
                    param = item.split(',')
                    if param[3]=='False':
                        queryset = queryset.filter()

            dic = queryset.aggregate(Min('price'), Max('price'))
            max_price = dic['price__max']
            min_price = dic['price__min']
            try:
                len = max_price - min_price
                step = len / 10
            except TypeError:
                step = False

            try:
                loaded_count = int(Settings.objects.get(name='loaded_count').value)
            except:
                loaded_count = 5

            result = GetLoadIds(queryset, loaded_count)
            splited_result = result.split('!')
            try:
                remaining_count = int(splited_result[0])
            except:
                remaining_count = False
            next_id_loaded_items = splited_result[1]

            items_html = render_to_string(
                'realestate/catalog_template.html',
                    {'catalog': queryset[:loaded_count], 'loaded_count': remaining_count, 'request': request,
                     'type': type, 'region': region, 'subtype': subtype,
                     'next_id_loaded_items': next_id_loaded_items,
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

        queryset = self.queryset

        dic = queryset.aggregate(Min('price'), Max('price'))
        context['max_price'] = dic['price__max']
        context['min_price'] = dic['price__min']
        try:
            len = context['max_price'] - context['min_price']
            context['step'] = len / 10
        except TypeError:
            context['step'] = False

        try:
            loaded_count = int(Settings.objects.get(name='loaded_count').value)
        except Settings.DoesNotExist:
            loaded_count = 5

        result = GetLoadIds(queryset, loaded_count)
        splited_result = result.split('!')
        try:
            remaining_count = int(splited_result[0])
        except:
            remaining_count = False
        next_id_loaded_items = splited_result[1]

        context['catalog'] = queryset[:loaded_count]
        context['loaded_count'] = remaining_count
        context['countries'] = ExclusiveRealEstate.objects.values('country').distinct().order_by('country')
        context['next_id_loaded_items'] = next_id_loaded_items
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
            if 'country' not in request.POST or 'country' not in request.POST and 'price_min' not in request.POST and 'price_max' not in request.POST:
                return HttpResponseBadRequest()

            if 'price_min' in request.POST and 'price_max' in request.POST:
                try:
                    price_min = int(request.POST['price_min'])
                    price_max = int(request.POST['price_max'])
                except:
                    return HttpResponseBadRequest()
            else:
                price_min = False
                price_max = False

            country = request.POST['country']
            if country == "all":
                queryset = ExclusiveRealEstate.objects.published()
            else:
                queryset = ExclusiveRealEstate.objects.filter(country=country)

            if price_min and price_max:
                queryset = queryset.filter(price__gte=price_min)
                queryset = queryset.filter(price__lte=price_max)

            dic = queryset.aggregate(Min('price'), Max('price'))
            max_price = dic['price__max']
            min_price = dic['price__min']
            try:
                len = max_price - min_price
                step = len / 10
            except TypeError:
                step = False

            try:
                loaded_count = int(Settings.objects.get(name='loaded_count').value)
            except Settings.DoesNotExist:
                loaded_count = 5

            result = GetLoadIds(queryset, loaded_count)
            splited_result = result.split('!')
            try:
                remaining_count = int(splited_result[0])
            except:
                remaining_count = False
            next_id_loaded_items = splited_result[1]

            items_html = render_to_string(
                'realestate/excl_catalog_template.html',
                    {'catalog': queryset[:loaded_count], 'loaded_count': remaining_count, 'request': request,
                     'next_id_loaded_items': next_id_loaded_items,
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
                html_code = u'%s<option value="%s">%s</option>' % (html_code, region.id, region.title)
            return HttpResponse(html_code)
        else:
            return HttpResponseBadRequest()

load_region = LoadRegionAdmin.as_view()

class ItemsLoaderView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect('/')
        else:
            if 'load_ids' not in request.POST or 'm_name' not in request.POST or 'a_name' not in request.POST:
                return HttpResponseBadRequest()

            load_ids = request.POST['load_ids']
            app_name = request.POST['a_name']
            model_name = request.POST['m_name']
            model = get_model(app_name, model_name)

            load_ids_list = load_ids.split('|')
            block_id = load_ids_list[0]
            load_ids = load_ids.replace(block_id, '')
            block_id = block_id.split(',')
            if load_ids.startswith(',') or load_ids.startswith('|'):
                load_ids = load_ids[1:]
            if load_ids.endswith(',') or load_ids.endswith('|'):
                load_ids = load_ids[:-1]

            try:
                next_ids = load_ids_list[1].split(',')
            except:
                next_ids = False

            if next_ids:
                remaining_count = len(next_ids)
            else:
                remaining_count = -1

            try:
                queryset = model.objects.published().filter(id__in=block_id)
            except model.DoesNotExist:
                return HttpResponseBadRequest()

            response = HttpResponse()
            load_template = 'items_loader/rre_load_template.html'
            items_html = render_to_string(
                'items_loader/base_loader.html',
                    {'items': queryset, 'load_template': load_template, 'remaining_count': remaining_count,
                     'load_ids': load_ids, }
            )
            response.content = items_html
            return response

items_loader = ItemsLoaderView.as_view()