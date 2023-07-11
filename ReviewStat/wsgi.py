"""
WSGI config for ReviewStat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import newrelic.agent

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReviewStat.settings')

application = get_wsgi_application()

newrelic.agent.register_application(timeout=10)