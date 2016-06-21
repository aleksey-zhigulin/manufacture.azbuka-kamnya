# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.fields import empty
from shop.rest.serializers import (ProductSummarySerializerBase, ProductDetailSerializerBase,
    AddToCartSerializer)
from shop.search.serializers import ProductSearchSerializer as ProductSearchSerializerBase
from .search_indexes import myshop_search_index_classes

Product = import_string('manufacture.models.products.product.Product')


class ProductSummarySerializer(ProductSummarySerializerBase):
    media = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_url', 'product_type', 'product_model', 'price',
                  'media',)

    def get_media(self, product):
        return self.render_html(product, 'media')


class ProductDetailSerializer(ProductDetailSerializerBase):
    class Meta:
        model = Product
        exclude = ('active',)


class ProductSearchSerializer(ProductSearchSerializerBase):
    """
    Serializer to search over all products in this shop
    """
    media = serializers.SerializerMethodField()

    class Meta(ProductSearchSerializerBase.Meta):
        fields = ProductSearchSerializerBase.Meta.fields + ('media',)
        index_classes = myshop_search_index_classes

    def get_media(self, search_result):
        return search_result.search_media


class CatalogSearchSerializer(ProductSearchSerializer):
    def get_media(self, search_result):
        return search_result.catalog_media
