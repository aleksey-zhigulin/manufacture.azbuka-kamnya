# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from shop.models.defaults.address import ShippingAddress, BillingAddress
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer
from .products.stone import Stone

from django.db import models
from django.utils.translation import ugettext_lazy as _

from zinnia.models_bases.entry import AbstractEntry
from cmsplugin_zinnia.placeholder import PlaceholderEntry
from filer.fields.image import FilerImageField
from orderedmodel import OrderedModel

class GalleryPicture(OrderedModel):
    entry = models.ForeignKey('zinnia.Entry', related_name='pictures')
    image = FilerImageField(verbose_name=_('Image'), related_name='+')
    alt_tag = models.CharField(_('Alt tag'), max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.alt_tag)


class Entry(PlaceholderEntry, AbstractEntry):

    class Meta(AbstractEntry.Meta):
        """
        EntryPlaceholder's Meta
        """
        abstract = True





