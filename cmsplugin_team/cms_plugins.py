from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import TeamPlugin

class CMSTeamPlugin(CMSPluginBase):
    model = TeamPlugin
    name = _("Team Item")
    module = _("Team")
    render_template = "cmsplugin_team/team_item.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
        })
        return context

plugin_pool.register_plugin(CMSTeamPlugin)
