# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

gettext = lambda s: s

BASE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))
WORK_DIR = os.environ.get('DJANGO_WORKDIR', PROJECT_ROOT)

SECRET_KEY = '-d!6*5=odhriaz_sk&z$+u_qnzi1(vof3k6!77i1s*$arx*dz^'

DEBUG = False

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True

# Application definition

ROOT_URLCONF = 'manufacture.urls'

WSGI_APPLICATION = 'manufacture.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'manufacture-azbuka-kamnya',
        'PASSWORD': 'kBcwGP53916',
        'PORT': '3306',
        'USER': 'admin'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(WORK_DIR, 'media')
STATIC_ROOT = os.path.join(WORK_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    ('bower_components', os.path.join(WORK_DIR,  'bower_components')),
    ('node_modules', os.path.join(WORK_DIR, 'node_modules')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
    'compressor.finders.CompressorFinder',
)

SITE_ID = 1

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'zinnia.context_processors.version',
                'shop.context_processors.customer',
                'shop.context_processors.version',
            ],
            'loaders': [
                # ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader'
                # ]),
            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'djng.middleware.AngularUrlMiddleware',
    # 'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shop.middleware.CustomerMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'polymorphic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.messages',

    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',

    'cmsplugin_yandexmap',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_forms_builder',
    'cmsplugin_carousel',
    'cmsplugin_lightboxgallery',
    'cmsplugin_service',
    'cmsplugin_stone',
    'cmsplugin_team',
    'cmsplugin_zinnia',


    'djangocms_text_ckeditor',
    'django_select2',
    'cmsplugin_cascade',
    'cmsplugin_cascade.clipboard',
    'cmsplugin_cascade.sharable',
    'cmsplugin_cascade.extra_fields',
    'cmsplugin_cascade.segmentation',
    'cms_bootstrap3',
    'adminsortable2',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_fsm',
    'fsm_admin',
    'djng',

    'django_comments',
    'mptt',
    'filer',
    'forms_builder.forms',
    'tagging',

    'reversion',
    'orderedmodel',
    'easy_thumbnails',
    'cms',
    'zinnia',
    'menus',
    'sekizai',
    'sass_processor',
    'compressor',
    'django_filters',
    'treebeard',
    'djangocms_rosetta',
    'rosetta',
    'robots',
    'memcache_admin',
    'easy_thumbnails.optimize',
    'parler',
    'post_office',
    'haystack',
    'shop',
    'manufacture',
    'currencies',
)


LANGUAGES = (
    ('ru', gettext('ru')),
)

############################################
# settings for caching backends

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

MIGRATION_MODULES = {

}

############################################
# settings for logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse',
         }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s %(module)s] %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs/django-errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'post_office': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

SILENCED_SYSTEM_CHECKS = ('auth.W004')

############################################
# settings for storing session data

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_SAVE_EVERY_REQUEST = True

############################################
# settings for third party apps

NODE_MODULES_URL = STATIC_URL + 'node_modules/'

SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(STATIC_ROOT, 'node_modules'),
    # os.path.join(PROJECT_ROOT, 'static/pages'),
)
SASS_PROCESSOR_ENABLED = True
# SASS_PROCESSOR_ROOT = os.path.join(PROJECT_ROOT, 'static')

COERCE_DECIMAL_TO_STRING = True

FSM_ADMIN_FORCE_PERMIT = True

COMPRESS_ROOT = STATIC_ROOT

from .cms import *
from .robots import *
from .rosetta import *
from .shop import *
from .zinnia import *
from .mail import *
from .rest_framework import *
from .filer import *
from .haystack import *

# merge settings with non-public credentioals in private_settings
for priv_attr in ('DATABASES', 'SECRET_KEY', 'EMAIL_HOST', 'EMAIL_PORT',
                  'EMAIL_HOST_USER', 'DEFAULT_FROM_EMAIL', 'EMAIL_HOST_PASSWORD', 'EMAIL_USE_TLS',
                  'EMAIL_REPLY_TO', 'EMAIL_BACKEND'):
    try:
        from . import private_settings
        vars()[priv_attr].update(getattr(private_settings, priv_attr))
    except AttributeError:
        continue
    except KeyError:
        vars()[priv_attr] = getattr(private_settings, priv_attr)
    except ImportError:
        break


if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }
