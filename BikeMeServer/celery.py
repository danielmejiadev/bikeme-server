#Activamos los imports absolutos para evitar conflictos entre packages 
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

#Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BikeMeServer.settings')

app = Celery('BikeMeServer')

#Añadimos el Django settings module como fuente de configuración de Celery (nos permite configurar Celery directamente desde el Django settings). Al pasarlo como string nos ahorramos un problema si trabajasemos con windows. 
app.config_from_object('django.conf:settings')

# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
