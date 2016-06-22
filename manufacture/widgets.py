from __future__ import absolute_import
from __future__ import unicode_literals

from collections import Iterable
from itertools import chain
try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode  # noqa

from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.widgets import flatatt
from django.utils.datastructures import MergeDict, MultiValueDict
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.six import string_types
from django.utils.translation import ugettext as _

import logging

logger = logging.getLogger('django')

class NgCheckboxSelectMultiple(forms.Widget):
    def __init__(self, attrs=None, choices=()):
        super(NgCheckboxSelectMultiple, self).__init__(attrs)

        self.choices = choices

    # def value_from_datadict(self, data, files, name):
    #     value = super(NgCheckboxSelectMultiple, self).value_from_datadict(data, files, name)
    #     self.data = data
    #     return value

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def render(self, name, value, attrs=None, choices=()):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        output = ['<ul%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        output.append('</ul>')
        return mark_safe('\n'.join(output))

    def render_options(self, choices, selected_choices, name):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for number, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            if isinstance(option_label, (list, tuple)):
                for option in option_label:
                    output.append(
                        self.render_option(name, number, selected_choices, *option))
            else:
                output.append(
                    self.render_option(name, number, selected_choices,
                                       option_value, option_label))
        return '\n'.join(output)

    def render_option(self, name, number, selected_choices,
                      option_value, option_label):
        option_value = force_text(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _("All")
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        return self.option_string() % {
             'attrs': selected and ' class="selected"' or '',
             'value': option_value,
             'label': force_text(option_label),
             'ng_model': 'property_filters.%s.value%s' % (name, number)
        }


    def option_string(self):
        return '''
        <li>
            <label>
                %(label)s
                <input type="checkbox"
                       ng-model="%(ng_model)s"
                       ng-true-value="'%(value)s'"
                       ng-false-value="''"
                       ng-change="filter()"
                       %(attrs)s>
            </label>
        </li>
        '''