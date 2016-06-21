from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ServicePlugin

class CMSServicesPlugin(CMSPluginBase):
    model = ServicePlugin
    name = _("Services")
    module = _("Services")
    render_template = "cmsplugin_service/service.html"

    def render(self, context, instance, placeholder):
        context.update({
            'auto_id': 'service_%s' % instance.pk,
            'object': instance,
        })
        return context

plugin_pool.register_plugin(CMSServicesPlugin)
