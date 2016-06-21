from django.contrib.sites.models import Site
from django.core.urlresolvers import NoReverseMatch, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from robots import settings
from robots.models import Rule
from robots.views import RuleList as RobotsRuleList

class RuleList(RobotsRuleList):
    def get_context_data(self, **kwargs):
        context = super(RuleList, self).get_context_data(**kwargs)
        context['sitemap_urls'] = self.get_sitemap_urls()
        host = self.current_site.domain
        if not host.startswith(('http', 'https')):
            scheme = self.request.is_secure() and 'https' or 'http'
            host = "%s://%s" % (scheme, host)
        context['host'] = host if settings.USE_HOST else None
        return context

rules_list = RuleList.as_view()


from __future__ import unicode_literals

import os
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.cache import add_never_cache_headers
from django.utils.translation import get_language_from_request
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.settings import api_settings
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from shop import settings as shop_settings
from shop.rest.money import JSONRenderer
from shop.rest.filters import CMSPagesFilterBackend
from shop.rest.serializers import AddToCartSerializer, ProductSelectSerializer
from shop.rest.renderers import CMSPageRenderer
from shop.models.product import ProductModel
from shop.views.catalog import ProductListView

class CMSPageProductListView(ProductListView):
    """
    This view is used to list all products being associated with a CMS page. It normally is
    added to the urlpatterns as:
    ``url(r'^$', CMSPageProductListView.as_view(serializer_class=ProductSummarySerializer))``
    where the ``ProductSummarySerializer`` is a customized REST serializer that that specific
    product model.
    """
    renderer_classes = (CMSPageRenderer, JSONRenderer, BrowsableAPIRenderer)
    filter_backends = list(api_settings.DEFAULT_FILTER_BACKENDS)
    filter_backends.append(CMSPagesFilterBackend())

    def filter_queryset(self, queryset):
        self.filter_context = None
        if self.filter_class:
            filter_instance = self.filter_class(self.request.query_params, queryset=queryset)
            if callable(getattr(filter_instance, 'get_render_context', None)):
                self.filter_context = filter_instance.get_render_context()
            elif hasattr(filter_instance, 'render_context'):
                self.filter_context = filter_instance.render_context
            assert(False)
        qs = super(CMSPageProductListView, self).filter_queryset(queryset)
        return qs

    def get_renderer_context(self):
        renderer_context = super(CMSPageProductListView, self).get_renderer_context()
        if renderer_context['request'].accepted_renderer.format == 'html':
            renderer_context['filter'] = self.filter_context
        return renderer_context
