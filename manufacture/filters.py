# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.utils import six
from django.utils.translation import ugettext_lazy as _

import django_filters
from django_filters import MultipleChoiceFilter
from django_filters import widgets
from django_filters.fields import Lookup

from manufacture.models.products.product import Product
from manufacture.widgets import NgCheckboxSelectMultiple
from manufacture.models.products.stone import StoneType

from logging import getLogger

logger = getLogger('django')


class AllValuesMultipleChoiceFilter(MultipleChoiceFilter):
    @property
    def field(self):
        qst = self.model._default_manager.distinct().order_by(self.name).values_list(self.name, flat=True)
        self.extra['choices'] = [(o, o) for o in qst if o]
        return super(AllValuesMultipleChoiceFilter, self).field

    def filter(self, qs, value):
        logger.error('value = %s' % str(value))
        value = value or ()  # Make sure we have an iterable
        if self.is_noop(qs, value):
            return qs

        # Even though not a noop, no point filtering if empty
        if not value:
            return qs
        q = Q()
        for v in set(value):
            if self.conjoined:
                qs = self.get_method(qs)(**{self.name: v})
            else:
                q |= Q(**{self.name: v})

        logger.error('q = %s' % q)
        if self.distinct:
            return self.get_method(qs)(q).distinct()

        return self.get_method(qs)(q)


class StoneFilter(django_filters.FilterSet):
    material = AllValuesMultipleChoiceFilter(label=_('Тип камня'),
                                             name='stonetype__stone_rock__name',
                                             widget=NgCheckboxSelectMultiple(attrs={'class': 'filter-material'})
                                             )
    color = AllValuesMultipleChoiceFilter(label=_('Цвет'),
                                          name='stonetype__stone_color__name',
                                          widget=NgCheckboxSelectMultiple)
    treatment = AllValuesMultipleChoiceFilter(label=_('Обработка'),
                                              name='stonetype__stone_treatment__name',
                                              widget=NgCheckboxSelectMultiple)
    country = AllValuesMultipleChoiceFilter(label=_('Страна'),
                                            name='stonetype__stone_country__name',
                                            widget=NgCheckboxSelectMultiple)
    # price_starts = django_filters.RangeFilter(label=_('Цена'), name='stonetype___price')

    def get_render_context(self):
        return self.form

    class Meta:
        model = Product
        fields = ['material', 'country', 'color', 'treatment']

