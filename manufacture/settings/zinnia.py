# -*- coding: utf-8 -*-
gettext = lambda s: s

ZINNIA_ENTRY_BASE_MODEL = 'manufacture.models.Entry'
ZINNIA_PAGINATION = 6
ZINNIA_COPYRIGHT = 'Азбука Камня'

ZINNIA_ENTRY_CONTENT_TEMPLATES = [('zinnia/_entry_detail_projects.html',
                                   gettext('Project')),]

ZINNIA_ENTRY_DETAIL_TEMPLATES = [
    ('entry_detail_project.html', gettext('Project')),
    ('entry_detail_news.html', gettext('News')),
]

ZINNIA_PROTOCOL = 'https'