from tamarcado.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
LOGGING = {
   **LOGGING,
   'loggers': {
      '': {  # Logger raiz
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
      }
   }
}