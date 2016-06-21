gettext = lambda s: s

CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'ru',
            'hide_untranslated': False,
            'name': gettext('ru'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('home.html', gettext('Home Page')),
    ('about.html', gettext('About')),
    ('blog.html', gettext('Blog')),
    ('contact.html', gettext('Contact')),
    ('gallery.html', gettext('Gallery')),
    ('single_project.html', gettext('Single project')),
    ('services.html', gettext('Services')),
    ('stone.html', gettext('Stone')),
    ('shop/pages/default.html', gettext("Shop")),
)

CMS_PERMISSION = False

CMS_CACHE_DURATIONS = {
    'content': 600,
    'menus': 3600,
    'permissions': 86400,
}

CMS_PERMISSION = False

CACSCADE_WORKAREA_GLOSSARY = {
    'breakpoints': ['xs', 'sm', 'md', 'lg'],
    'container_max_widths': {'xs': 750, 'sm': 750, 'md': 970, 'lg': 1170},
    'fluid': False,
    'media_queries': {
        'xs': ['(max-width: 768px)'],
        'sm': ['(min-width: 768px)', '(max-width: 992px)'],
        'md': ['(min-width: 992px)', '(max-width: 1200px)'],
        'lg': ['(min-width: 1200px)'],
    },
}

CMS_PLACEHOLDER_CONF = {
    'Breadcrumb': {
        'plugins': ['BreadcrumbPlugin'],
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
    'Product Details': {
        'plugins': ['BootstrapContainerPlugin'],
        'text_only_plugins': ['TextLinkPlugin'],
        'parent_classes': {'BootstrapContainerPlugin': None},
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
    'Main Content Container': {
        'plugins': ['BootstrapContainerPlugin'],
        'text_only_plugins': ['TextLinkPlugin'],
        'parent_classes': {'BootstrapContainerPlugin': None},
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
}


CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.segmentation', 'cmsplugin_cascade.generic',
                             'cmsplugin_cascade.link', 'shop.cascade', 'cmsplugin_cascade.bootstrap3',)


CMSPLUGIN_CASCADE = {
    'dependencies': {
        'shop/js/admin/shoplinkplugin.js': 'cascade/js/admin/linkpluginbase.js',
    },
    'alien_plugins': ('TextPlugin', 'TextLinkPlugin',),
    'bootstrap3': {
        'template_basedir': 'angular-ui',
    },
    'plugins_with_extra_fields': (
        'BootstrapButtonPlugin',
        'BootstrapRowPlugin',
        'SimpleWrapperPlugin',
        'HorizontalRulePlugin',
        'ExtraAnnotationFormPlugin',
        'ShopProceedButton',
    ),
    'segmentation_mixins': (
        ('shop.cascade.segmentation.EmulateCustomerModelMixin', 'shop.cascade.segmentation.EmulateCustomerAdminMixin'),
    ),
}

CMSPLUGIN_CASCADE_LINKPLUGIN_CLASSES = (
    'shop.cascade.plugin_base.CatalogLinkPluginBase',
    'cmsplugin_cascade.link.plugin_base.LinkElementMixin',
    'shop.cascade.plugin_base.CatalogLinkForm',
)

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'skin': 'moono',
    'toolbar': 'CMS',
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
}

SELECT2_CSS = 'bower_components/select2/dist/css/select2.min.css'
SELECT2_JS = 'bower_components/select2/dist/js/select2.min.js'
