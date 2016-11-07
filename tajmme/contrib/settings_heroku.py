"""
Django settings for Tajm, Heroku flavoured.

For more information on this file, see
https://github.com/etianen/django-herokuapp

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from semirhage.settings import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}