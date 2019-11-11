import os
import time
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zaphiemieg2xae4ohze7chakui8yohGen2oohaiVae6va7auzoh7ejaiph4These'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


ADMINS = [('Admin', '')]
SERVER_EMAIL = ''
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX = '[NOTES] '
EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''


# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',     # to enable/disable imgur/custom uploader.
    'mention': 'true',  # to enable/disable mention
    'jquery': 'true',    # to include/revoke jquery (require for admin default django)
}

MARTOR_UPLOAD_PATH = 'uploads/{}'.format(time.strftime("%Y/%m/%d/"))
MARTOR_UPLOAD_URL = '/uploader/'
MAX_IMAGE_UPLOAD_SIZE = 20971520  # 20MB

# Telegram Setting
BOT_TOKEN = ''
ADMIN_ID = ''  # telegram id админа, для отправки с формы пожеланий
CHAT_ID = ''   # telegram id чата для модераторов (падают новые заметки на публикацию)


# Auth
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60
ACCOUNT_EMAIL_MAX_LENGTH = 190
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_USERNAME_BLACKLIST = ['admin']
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_ADAPTER = 'evernote.models.MyAccountAdapter'

# Redirect after login
LOGIN_REDIRECT_URL = '/'


sys.path.insert(0, os.path.join(BASE_DIR, 'apps/'))
# Application definition
CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'widget_tweaks',
    'martor',
]

PROJECT_APPS = [
    'notes',
    'users_notes',
    'search',
    'moderator',
    'uploader',
]

INSTALLED_APPS = CORE_APPS + PROJECT_APPS

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'evernote.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'evernote.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'POST': '3306',
        'OPTIONS': {
                'sql_mode': 'traditional',
        }
    }
}


# Password validation
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

LANGUAGE_CODE = 'ru_Ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = "d M Y H:i"

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
