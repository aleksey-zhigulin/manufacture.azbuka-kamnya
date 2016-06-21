# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import forms_builder.forms.urls
from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from manufacture.views import rules_list


admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^rosetta/', include('rosetta.urls')),
                       url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
                       url(r'^comments/', include('django_comments.urls')),
                       url(r'^admin/', include(admin.site.urls)),  # NOQA
                       url(r'^forms/', include(forms_builder.forms.urls)),
                       url(r'^robots\.txt$', rules_list, name='robots_rule_list'),
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
                           {'sitemaps': {
                               'cmspages': CMSSitemap,
                               'tags': TagSitemap,
                               'blog': EntrySitemap,
                               'categories': CategorySitemap,
                           }}),
                       url(r'^select2/', include('django_select2.urls')),
                       url(r'^', include('cms.urls')),
                       url(r'^stone/', include('shop.urls', namespace='shop')),
                       )


# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           ) + staticfiles_urlpatterns() + urlpatterns  # NOQA
