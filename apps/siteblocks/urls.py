# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from views import LatestNewsFeed

urlpatterns = patterns('apps.siteblocks.views',
    url(r'^/rss/$', LatestNewsFeed(), name='rss', ),
    url(r'^/$', 'news_list', name='news_list', ),
    url(r'^/view/(?P<pk>\d*)/$', 'news_detail', name='news_detail'),

)
