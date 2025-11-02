# projeto/settings.py

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(os.path.join(BASE_DIR, '.env'))
# --- Chaves e Configurações de Ambiente ---
# A SECRET_KEY é lida da variável de ambiente no Render.
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG é False em produção, a menos que a variável de ambiente DEBUG seja 'True'.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'


if DEBUG:
    # Se estiver em desenvolvimento (DEBUG=True), permita o localhost
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    # Se estiver em produção (DEBUG=False), use a URL do Render
    ALLOWED_HOSTS = ['projetos2-jc-rec-o.onrender.com']


# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuario',
    'jornal_commercio',
    'whitenoise.runserver_nostatic', # Adicionado para servir arquivos estáticos
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # DEVE SER A SEGUNDA LINHA
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'jornal_commercio.context_processors.global_feedback_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# --- Database ---
# Usa dj_database_url para ler a variável DATABASE_URL do Render.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', # Banco de dados para desenvolvimento local
        conn_max_age=600
    )
}


# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_REDIRECT_URL = 'perfil'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'


# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuração do Whitenoise para servir arquivos estáticos em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'