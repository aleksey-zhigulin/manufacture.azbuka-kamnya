from django.contrib.sites.models import Site
from django.core.urlresolvers import NoReverseMatch, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from robots import settings
from robots.models import Rule
from robots.views import RuleList as RobotsRuleList

class RuleList(RobotsRuleList):
    def get_context_data(self, **kwargs):
        context = super(RuleList, self).get_context_data(**kwargs)
        context['sitemap_urls'] = self.get_sitemap_urls()
        host = self.current_site.domain
        if not host.startswith(('http', 'https')):
            scheme = self.request.is_secure() and 'https' or 'http'
            host = "%s://%s" % (scheme, host)
        context['host'] = host if settings.USE_HOST else None
        return context

rules_list = RuleList.as_view()



