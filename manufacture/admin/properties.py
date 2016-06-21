# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from manufacture.models.properties import Country, Color, Type, Treatment, Size, Rock, Stock, Thickness


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Rock)
class RockAdmin(admin.ModelAdmin):
    pass

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass

@admin.register(Thickness)
class ThicknessAdmin(admin.ModelAdmin):
    pass
