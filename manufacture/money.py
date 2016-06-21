# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import python_2_unicode_compatible
from decimal import Decimal, InvalidOperation
from cms.utils.helpers import classproperty
from shop import settings as shop_settings
from shop.money.money_maker import AbstractMoney

CURRENCIES = {
    'AUD': ('036', 2, '$', _("Australian Dollar")),
    'BRL': ('986', 2, 'R$', _("Brazilian Real")),
    'CHF': ('756', 2, 'SFr.', _("Swiss Franc")),
    'CNY': ('156', 2, '¥', _("Chinese Yuan")),
    'CZK': ('203', 2, 'Kč', _("Czech Koruna")),
    'EUR': ('978', 2, '€', _("Euro")),
    'GBP': ('826', 2, '£', _("Pound Sterling")),
    'HUF': ('348', 0, 'Ft', _("Hungarian Forint")),
    'ILS': ('376', 2, '₪', _("Israeli Sheqel")),
    'JPY': ('392', 0, '¥', _("Japanese Yen")),
    'RUB': ('643', 0, '₽', _("Russian Ruble")),
    'UAH': ('980', 2, '₴', _("Ukrainian Hryvnia")),
    'USD': ('840', 2, '$', _("US Dollar")),
    # feel free to add more currencies, alphabetically ordered
}

class MoneyMaker(type):
    """
    Factory for building Decimal types, which keep track of the used currency. This is to avoid
    unintentional price allocations, when combined with decimals or when working in different
    currencies.

    No automatic conversion of currencies has been implemented. This could however be achieved
    quite easily in a separate shop plugin.
    """
    def __new__(cls, currency_code=None):
        def new_money(cls, value='NaN', context=None):
            """
            Build a class named MoneyIn<currency_code> inheriting from Decimal.
            """
            if isinstance(value, cls):
                assert cls._currency_code == value._currency_code, "Money type currency mismatch"
            if value is None:
                value = 'NaN'
            try:
                self = Decimal.__new__(cls, value, context)
            except Exception as err:
                raise ValueError(err)
            return self

        if currency_code is None:
            currency_code = shop_settings.DEFAULT_CURRENCY
        else:
            currency_code = currency_code.upper()
        if currency_code not in CURRENCIES:
            raise ValueError("'{}' is an unknown currency code. Please check shop/money/iso4217.py".format(currency_code))
        name = str('MoneyIn' + currency_code)
        bases = (AbstractMoney,)
        try:
            cents = Decimal('.' + CURRENCIES[currency_code][1] * '0')
        except InvalidOperation:
            # Currencies with no decimal places, ex. JPY, HUF
            cents = Decimal()
        attrs = {'_currency_code': currency_code, '_currency': CURRENCIES[currency_code],
                 '_cents': cents, '__new__': new_money}
        new_class = type(name, bases, attrs)
        return new_class
