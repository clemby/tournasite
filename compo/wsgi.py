"""
WSGI config for compo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import logging
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compo.settings")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)

logging.basicConfig(stream=sys.stderr)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
