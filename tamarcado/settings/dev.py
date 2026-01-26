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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='0.0.0.0'
EMAIL_PORT = 1025