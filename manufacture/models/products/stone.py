# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop.money import Money
from filer.fields.image import FilerImageField
from cms.models.fields import PlaceholderField
from manufacture.money import MoneyMaker
from shop import settings as shop_settings

from .product import Product
from manufacture.models.properties import Color, Country, Size, Treatment, Type, Rock, Stock, Thickness
from currencies.models import Currency, Rate

class StoneType(Product):
    stone_country = models.ForeignKey(Country,
                                      verbose_name=_("Страна производитель"), null=True, blank=True)
    stone_color = models.ForeignKey(Color,
                                    verbose_name=_("Цвет"), null=True, blank=True)
    stone_rock = models.ForeignKey(Rock,
                                   verbose_name=_("Порода камня"), null=True, blank=True)
    stone_treatment = models.ForeignKey(Treatment,
                                        verbose_name=_("Обработка"), null=True, blank=True)

    placeholder = PlaceholderField("Product Details")

    class Meta:
        verbose_name = _("Stone")
        verbose_name_plural = _("Stones ")

    def get_price(self, request):
        if not hasattr(self, '_price'):
            if self.stone_set.exists():
                currency = shop_settings.DEFAULT_CURRENCY
                self._price = MoneyMaker(currency)(min(i.converted_price for i in self.stone_set.all()))
            else:
                self._price = Money()
        return self._price

    def get_product_variant(self, product_code):
        try:
            return self.stone_set.get(product_code=product_code)
        except Stone.DoesNotExist as e:
            raise Stone.DoesNotExist(e)

    def get_stocks(self):
        if not self.stone_set.exists(): return None
        products = OrderedDict()
        for stock in Stock.objects.all():
            products[stock.name] = self.stone_set.filter(stock=stock.id)
        return products


class Stone(models.Model):
    type = models.ForeignKey(StoneType,
                             verbose_name=_("Вид камня"))
    unit_price = models.DecimalField(_("Цена"), decimal_places=2, max_digits=30, default=0,
                            help_text=_("Цена за кватратный метр"))
    currency = models.ForeignKey(Currency, related_name='+')
    stock = models.ForeignKey(Stock,
                              verbose_name=_("Склад"))
    stone_form = models.ForeignKey(Type,
                                   verbose_name=_("Тип камня"))
    stone_size = models.ForeignKey(Size,
                                   verbose_name=_("Размер"))
    stone_thickness = models.ForeignKey(Thickness,
                                   verbose_name=_("Толщина"), null=True, blank=True)

    image = FilerImageField(verbose_name=_('Image'), null=True, blank=True, related_name='+')

    @property
    def converted_price(self):
        currency = shop_settings.DEFAULT_CURRENCY
        if self.currency.code != 'RUB':
            return MoneyMaker(currency)(self.unit_price * self.currency.rate.value // 1)
        return MoneyMaker(currency)(self.unit_price // 1)

    @property
    def form_and_thickness(self):
        if self.stone_form.name == 'Слэб':
            return '%s %s' % (self.stone_form, self.stone_thickness)
        return self.stone_form

    def get_price(self, request):
        return self.converted_price

    def __unicode__(self):
        return '%s - %s' % (self.stone_form, self.stone_size)