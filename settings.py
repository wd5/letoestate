# -*- coding: utf-8 -*-
DATABASE_NAME = u'letoestate'
PROJECT_NAME = u'letoestate'
SITE_NAME = u'LetoEstate'
SITE_URL = u'letoestate.ru'
DEFAULT_FROM_EMAIL = u'support@letoestate.ru'

from config.base import *

try:
    from config.development import *
except ImportError:
    from config.production import *

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'apps.siteblocks',
    'apps.pages',
    'apps.faq',
    'apps.slider',
    'apps.realestate',
    'django.contrib.sitemaps',

    'sorl.thumbnail',
    #'south',
    #'captcha',
)

MIDDLEWARE_CLASSES += (
    'apps.pages.middleware.PageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'apps.pages.context_processors.meta',
    'apps.siteblocks.context_processors.settings',
)