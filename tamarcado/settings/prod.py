import os
import dj_database_url
from tamarcado.settings.base import *

# -------------------------------
# Configurações de produção
# -------------------------------

DEBUG = False

# Chave secreta do Django
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key")

# Hosts permitidos
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(" ")

# Configuração do banco de dados usando DATABASE_URL
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# -------------------------------
# Arquivos estáticos e mídia
# -------------------------------

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Diretórios onde os arquivos serão coletados
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -------------------------------
# Middleware e armazenamento
# -------------------------------

# Adiciona Whitenoise para servir arquivos estáticos
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Configura o armazenamento de arquivos estáticos para compressão e caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
