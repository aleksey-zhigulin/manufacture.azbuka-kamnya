# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from shop.views.catalog import CMSPageProductListView, ProductRetrieveView
from shop.search.views import SearchView
from manufacture.serializers import (ProductSummarySerializer, ProductDetailSerializer, CatalogSearchSerializer)
from manufacture.filters import StoneFilter


urlpatterns = patterns('',
    url(r'^$', CMSPageProductListView.as_view(
        serializer_class=ProductSummarySerializer,
        filter_class=StoneFilter,
    )),
    url(r'^search-catalog$', SearchView.as_view(
        serializer_class=CatalogSearchSerializer,
    )),
    url(r'^(?P<slug>[\w-]+)$', ProductRetrieveView.as_view(
        serializer_class=ProductDetailSerializer,
    )),
)
