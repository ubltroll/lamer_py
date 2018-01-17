"""
WSGI config for lamer_py project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lamer_py.settings")

sys.path.insert(0,PROJECT_DIR)
PROJECT_DIR = dirname(dirname(abspath(__file__)))
application = get_wsgi_application()
