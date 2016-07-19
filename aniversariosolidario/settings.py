import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1kgvk#nk@ah4jd^s227j399#aj-r8&v6s4l8*$si+!y)#b4*^+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'ordered_model',
    'pagseguro',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'usuarios',
    'nucleo',
    'financeiro',
    'webapp',
    'emails',
    'easy_thumbnails',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aniversariosolidario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'nucleo.context_processors.taxa',
            ],
        },
    },
]

WSGI_APPLICATION = 'aniversariosolidario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Auth

AUTH_USER_MODEL = 'usuarios.Usuario'

LOGIN_URL = '/usuario/entrar/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_ADAPTER = 'usuarios.adapter.UsuarioSocialAccountAdapter'
ACCOUNT_ADAPTER = 'usuarios.adapter.UsuarioAccountAdapter'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# SITE INFO

PROTOCOL = 'http'
SITE_DOMAIN = 'localhost:8000'

# ARQUIVOS PERMITIDOS EM MEDIAS

MEDIA_IMAGENS_TYPES = [
    'image/jpeg',
    'image/png'
]

MEDIA_VIDEOS_TYPES = []

# PAGSEGURO

PAGSEGURO_EMAIL = 'douglas.paz.net@gmail.com'
PAGSEGURO_TOKEN = '5560FA1076914B6F98DBD3BC7FEC222E'
PAGSEGURO_SANDBOX = True
PAGSEGURO_LOG_IN_MODEL = True

# CONFIG

TAXA = .12

try:
    from local_settings import *
except:
    pass

FULL_URL = '{}://{}'.format(PROTOCOL, SITE_DOMAIN)

MEDIA_TYPES = MEDIA_IMAGENS_TYPES + MEDIA_VIDEOS_TYPES

TAXA_VERBOSE = u'{}%'.format('%.0f' % (TAXA * 100))