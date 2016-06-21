import django_filters
from django_filters import widgets
from manufacture.models.products.product import Product

class StoneFilter(django_filters.FilterSet):
    material = django_filters.AllValuesFilter(name='stonetype__stone_rock__name', widget=widgets.LinkWidget)
    color = django_filters.AllValuesFilter(name='stonetype__stone_color__name', widget=widgets.LinkWidget)
    treatment = django_filters.AllValuesFilter(name='stonetype__stone_treatment__name', widget=widgets.LinkWidget)
    country = django_filters.AllValuesFilter(name='stonetype__stone_country__name', widget=widgets.LinkWidget)

    class Meta:
        model = Product
        fields = ['material', 'country', 'color', 'country']

