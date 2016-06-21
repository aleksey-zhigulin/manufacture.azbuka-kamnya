from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from filer.fields.image import FilerImageField


class TeamPlugin(CMSPlugin):
    name = models.CharField(_('Title'), max_length=255, default='', blank=True)
    post = models.CharField(_('Postition'), max_length=255, default='', blank=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    image = FilerImageField(verbose_name=_('Image'))

    def __unicode__(self):
        return unicode(self.name or self.pk)

