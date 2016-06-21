# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from shop.search.indexes import ProductIndex as ProductIndexBase
from haystack import indexes

from manufacture.models.products.stone import StoneType


class ProductIndex(ProductIndexBase):
    catalog_media = indexes.CharField(stored=True, indexed=False, null=True)
    search_media = indexes.CharField(stored=True, indexed=False, null=True)

    def prepare_catalog_media(self, product):
        return self.render_html('catalog', product, 'media')

    def prepare_search_media(self, product):
        return self.render_html('search', product, 'media')


class StoneIndex(ProductIndex, indexes.Indexable):
    def get_model(self):
        return StoneType


myshop_search_index_classes = (StoneIndex,)

