from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.models.fields import PageField

from filer.fields.image import FilerImageField
from orderedmodel import OrderedModel


class ServicePlugin(CMSPlugin):
    title = models.CharField(_('Title'), max_length=255, default='', blank=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    image = FilerImageField(verbose_name=_('Image'), related_name='+')
    alt_tag = models.CharField(_('Alt tag'), max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.title or self.pk)

