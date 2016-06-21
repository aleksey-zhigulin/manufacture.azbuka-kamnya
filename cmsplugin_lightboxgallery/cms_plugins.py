from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GalleryPlugin, GalleryPicture


class PictureInline(admin.TabularInline):
    model = GalleryPicture
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.TextField):
            modified_text_field = db_field.formfield()
            modified_text_field.widget = forms.Textarea(attrs={'cols': 30, 'rows': 3})
            return modified_text_field
        return super(PictureInline, self).formfield_for_dbfield(db_field, **kwargs)


class CMSGalleryPlugin(CMSPluginBase):
    model = GalleryPlugin
    name = _("lightbox")
    module = _("Gallery")
    render_template = "cmsplugin_lightboxgallery/lightbox.html"

    inlines = [PictureInline]

    def render(self, context, instance, placeholder):
        context.update({
            'objects_list': instance.pictures.select_related('image'),
        })
        return context

plugin_pool.register_plugin(CMSGalleryPlugin)
