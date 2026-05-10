import os
from django.apps import AppConfig


class ErmaConfig(AppConfig):
    name = 'apps.eRMA'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from apps.eRMA.flows.automation.navegation import SessionManager
        SessionManager.instance()