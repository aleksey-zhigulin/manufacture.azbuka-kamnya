from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import StonePlugin

class CMSStonePlugin(CMSPluginBase):
    model = StonePlugin
    name = _("Stone Item")
    module = _("Stone")
    render_template = "cmsplugin_stone/stone.html"

    def render(self, context, instance, placeholder):
        context.update({
            'auto_id': 'stone_%s' % instance.pk,
            'object': instance,
        })
        return context

plugin_pool.register_plugin(CMSStonePlugin)
