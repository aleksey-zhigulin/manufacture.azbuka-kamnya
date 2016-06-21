# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from shop.admin.customer import CustomerProxy, CustomerAdmin
from shop.models.order import OrderModel
from . import properties

from .products import product

admin.site.register(CustomerProxy, CustomerAdmin)

#ZINNIA ADMIN
from django.contrib import admin
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cms.plugin_rendering import render_placeholder
from cms.admin.placeholderadmin import PlaceholderAdminMixin

from zinnia.models import Entry
from zinnia.admin.entry import EntryAdmin as CoreEntryAdmin
from zinnia.settings import ENTRY_BASE_MODEL

from manufacture.models import GalleryPicture

class GalleryInline(admin.TabularInline):
    model = GalleryPicture


class EntryAdmin(PlaceholderAdminMixin, CoreEntryAdmin):
    """
    EntryPlaceholder Admin
    """
    fieldsets = (
        (_('Content'), {'fields': (('title', 'status'), 'image')}),) + \
        CoreEntryAdmin.fieldsets[1:]
    inlines = [GalleryInline,]

    def save_model(self, request, entry, form, change):
        """
        Fill the content field with the interpretation
        of the placeholder
        """
        context = RequestContext(request)
        try:
            content = render_placeholder(entry.content_placeholder, context)
        except KeyError:
            content = None
        entry.content = content or ''
        super(EntryAdmin, self).save_model(
            request, entry, form, change)


if ENTRY_BASE_MODEL == 'manufacture.models.Entry':
    admin.site.register(Entry, EntryAdmin)