# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(_("Страна производитель"), max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Color(models.Model):
    name = models.CharField(_("Цвет"), max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Treatment(models.Model):
    name = models.CharField(_("Обработка"), max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Size(models.Model):
    name = models.CharField(_("Размер"), max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Type(models.Model):
    name = models.CharField(_("Тип камня"), max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Rock(models.Model):
    name = models.CharField(_("Порода камня"), max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Stock(models.Model):
    name = models.CharField(_("Склад"), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

@python_2_unicode_compatible
class Thickness(models.Model):
    name = models.CharField(_("Толщина"), max_length=50)

    def __str__(self):
        return self.name