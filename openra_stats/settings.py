"""
Django settings for openra_stats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!3q3n4i7endl-y22pwlt64_dgfkq1vqjf07$8&n2cyp)pk=q)2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'registration',
    'djangobower',
    'rest_framework',

    'tourn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages'
)

ROOT_URLCONF = 'openra_stats.urls'

WSGI_APPLICATION = 'openra_stats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# You need to define DATABASES this in ./local_settings.py.
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# registration provides templates for the registration app, and
# openra_stats/templates (for base.html) isn't included by default.
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'openra_stats/templates'),
    os.path.join(BASE_DIR, 'registration/templates'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# There seems to be a bug(?) in djangobower which always appends
# 'bower_components' to the end of this. Then the os.path.exists check for
# <BASE_DIR>/bower_components/bower_components fails, and it ends up looking in
# <BASE_DIR>/bower_components/components/ which is VERY annoying.
BOWER_COMPONENTS_ROOT = BASE_DIR


def get_bower_components():
    components = []
    with open('bower.json', 'r') as bower_file:
        dependencies = json.load(bower_file)['dependencies']
        for name, version in dependencies.items():
            dep = name if version == '*' else '{}#{}'.format(name, version)
            components.append(dep)

    return tuple(components)

BOWER_INSTALLED_APPS = get_bower_components()


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
}


# django-registration-redux options
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_AUTO_LOGIN = False


# For django.contrib.sites
SITE_ID = 1


from local_settings import *  # nopep8
