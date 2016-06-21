from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

from filer.fields.image import FilerImageField
from orderedmodel import OrderedModel


class GalleryPlugin(CMSPlugin):
    title = models.CharField(_('Title'), max_length=255, default='', blank=True)

    def __unicode__(self):
        return unicode(self.title or self.pk)

    def copy_relations(self, oldinstance):
        super(GalleryPlugin, self).copy_relations(oldinstance)
        for picture in oldinstance.pictures.all().iterator():
            picture.pk = None
            picture.plugin = self
            picture.save()


class GalleryPicture(OrderedModel):
    plugin = models.ForeignKey(GalleryPlugin, related_name='pictures')
    image = FilerImageField(verbose_name=_('Image'), related_name='+')
    alt_tag = models.CharField(_('Alt tag'), max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.alt_tag)
