import os
import dj_database_url
from tamarcado.settings.base import *

# -------------------------------
# Configurações de produção
# -------------------------------

DEBUG = False

# Chave secreta do Django
# No Render, defina a variável de ambiente DJANGO_SECRET_KEY
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Hosts permitidos
# O Render define RENDER_EXTERNAL_HOSTNAME automaticamente
ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")]

# Adiciona o host do serviço do Render para health checks
RENDER_INTERNAL_HOSTNAME = os.environ.get('RENDER_INTERNAL_HOSTNAME')
if RENDER_INTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_INTERNAL_HOSTNAME)

# Configuração do banco de dados usando DATABASE_URL
# No Render, crie um serviço de banco de dados e use sua "Internal Connection URL"
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# Confiar no proxy do Render para SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# -------------------------------
# Arquivos estáticos e mídia
# -------------------------------

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Diretórios onde os arquivos serão coletados
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles") # Mudado para evitar conflito com a pasta de mídia local

# -------------------------------
# Middleware e armazenamento
# -------------------------------

# Adiciona Whitenoise para servir arquivos estáticos
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Configura o armazenamento de arquivos estáticos para compressão e caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------
# Email
# -------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise RuntimeError("REDIS_URL não definida")
