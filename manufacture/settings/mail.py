# -*- coding: utf-8 -*-

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@azbuka-kamnya.ru'
EMAIL_HOST_PASSWORD = 'kBcwGP'
DEFAULT_FROM_EMAIL = 'Азбука Камня <noreply@azbuka-kamnya.ru>'
EMAIL_REPLY_TO = 'business@azbuka-kamnya.ru'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = 'post_office.EmailBackend'