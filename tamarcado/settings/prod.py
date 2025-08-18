from tamarcado.settings.base import *
import os
import dj_database_url

DEBUG = False

# Railway cria um domínio temporário (ex: yourapp.up.railway.app)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(" ")

# Banco de dados (Railway fornece DATABASE_URL)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,  # mantém conexões abertas
        ssl_require=True   # importante para produção
    )
}

# Static e Media
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Whitenoise para servir arquivos estáticos no Railway
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Secret key via variável de ambiente
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key")
