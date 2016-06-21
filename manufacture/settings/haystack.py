HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'shop',
    },
}

HAYSTACK_ROUTERS = ('shop.search.routers.LanguageRouter',)
