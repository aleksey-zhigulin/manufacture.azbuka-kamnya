# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy  as _

from urllib2 import urlopen
import xml.etree.ElementTree as ET
from currencies.models import Rate

class Command(BaseCommand):
    help = _('Daily update currency exchange rates')

    def handle(self, *args, **options):
        update_rate()


def update_rate():
    cbr_url='http://www.cbr.ru/scripts/XML_daily.asp'
    cbr_xml=urlopen(cbr_url).read()
    root = ET.fromstring(cbr_xml)

    usd = Rate.objects.get(currency__code='USD')
    if usd:
        usd.rate = root.find("Valute[@ID='R01235']/Value").text.replace(',', '.')
        usd.save()
    eur = Rate.objects.get(currency__code='EUR')
    if eur:
        eur.rate = root.find("Valute[@ID='R01239']/Value").text.replace(',', '.')
        eur.save()

