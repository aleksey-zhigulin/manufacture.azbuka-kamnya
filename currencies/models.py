# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_noop as _


class Currency(models.Model):
    name = models.CharField(_("Валюта"), max_length=20, unique=True)
    code = models.CharField(_("Код валюты"), max_length=3, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Валюта")
        verbose_name_plural = _("Валюты")


class Rate(models.Model):
    currency = models.OneToOneField(Currency, related_name='rate')
    value = models.DecimalField(_("Курс"), decimal_places=2, max_digits=30, default=0)

    def __unicode__(self):
        return self.currency.name

    class Meta:
        verbose_name = _("Курс валюты")
        verbose_name_plural = _("Курсы валют")

