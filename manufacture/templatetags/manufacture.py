"""Template tags and filters for Zinnia"""
import re
from hashlib import md5
from datetime import date
try:
    from urllib.parse import urlencode
except ImportError:  # Python 2
    from urllib import urlencode

from django.db.models import Q
from django.db.models import Count
from django.conf import settings
from django.utils import timezone
from django.template import Library
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.html import conditional_escape
from django.template.loader import select_template
from django.template.defaultfilters import stringfilter
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from django_comments.models import CommentFlag
from django_comments import get_model as get_comment_model

from tagging.models import Tag
from tagging.utils import calculate_cloud


from zinnia.models.entry import Entry
from zinnia.comparison import EntryPublishedVectorBuilder


WIDONT_REGEXP = re.compile(
    r'\s+(\S+\s*)$')
DOUBLE_SPACE_PUNCTUATION_WIDONT_REGEXP = re.compile(
    r'\s+([-+*/%=;:!?]+&nbsp;\S+\s*)$')
END_PUNCTUATION_WIDONT_REGEXP = re.compile(
    r'\s+([?!]+\s*)$')

register = Library()

@register.inclusion_tag('zinnia/tags/dummy.html')
def get_random_entries_in_category(number=5, template='zinnia/tags/entries_random.html', category='', title=None):
    """
    Return random entries.
    """
    return {'template': template,
            'entries': Entry.published.search('category:'+category).order_by('?')[:number],
            'title': title}

@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_similar_entries_in_category(context, number=5,
                        template='zinnia/tags/entries_similar.html', category=''):
    """
    Return similar entries.
    """
    entry = context.get('entry')
    if not entry:
        return {'template': template, 'entries': []}

    vectors = EntryPublishedVectorBuilder(queryset=Entry.published.search('category:'+category))
    entries = vectors.get_related(entry, number)

    return {'template': template,
            'entries': entries}
