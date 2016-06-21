# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db.models import Max
from django.template.context import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableAdminMixin
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin
from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter)
from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline
from manufacture.models.products.product import Product
from manufacture.models.products.stone import Stone, StoneType




class StoneInline(admin.StackedInline):
    model = Stone
    extra = 0


class StoneTypeAdmin(SortableAdminMixin, TranslatableAdmin, FrontendEditableAdminMixin,
                      CMSPageAsCategoryMixin, PlaceholderAdminMixin, PolymorphicChildModelAdmin):
    base_model = Product
    fieldsets = (
        (None, {
            'fields': ('product_name', 'slug', 'active',),
        }),
        (_("Translatable Fields"), {
            'fields': ('description',)
        }),
        (_("Properties"), {
            'fields': ('stone_rock', 'stone_country', 'stone_color', 'stone_treatment'),
        }),
    )
    filter_horizontal = ('cms_pages',)
    inlines = (ProductImageInline, StoneInline,)
    prepopulated_fields = {'slug': ('product_name',)}

    def save_model(self, request, obj, form, change):
        if not change:
            # since SortableAdminMixin is missing on this class, ordering has to be computed by hand
            max_order = self.base_model.objects.aggregate(max_order=Max('order'))['max_order']
            obj.order = max_order + 1 if max_order else 1
        super(StoneTypeAdmin, self).save_model(request, obj, form, change)

    def render_text_index(self, instance):
        template = get_template('search/indexes/manufacture/commodity_text.txt')
        return template.render(Context({'object': instance}))
    render_text_index.short_description = _("Text Index")


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, PolymorphicParentModelAdmin):
    base_model = Product
    child_models = ((StoneType, StoneTypeAdmin),)
    list_display = ('product_name', 'get_price', 'product_type', 'active',)
    list_display_links = ('product_name',)
    search_fields = ('product_name',)
    list_filter = (PolymorphicChildModelFilter,)
    list_per_page = 250
    list_max_show_all = 1000

    def get_price(self, obj):
        return obj.get_real_instance().get_price(None)
    get_price.short_description = _("Price starting at")
