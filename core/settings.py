# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
# ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1',               env('SERVER', default='127.0.0.1') ]
# CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + env('SERVER', default='127.0.0.1') ]
ALLOWED_HOSTS=['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'apps.home',                                  # Enable the inner home (home)
    'allauth',                                      # OAuth new
    'allauth.account',                              # OAuth new
    'allauth.socialaccount',                        # OAuth new 
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',       # OAuth new 
    "sslserver",                                    
    'rest_framework',
    'rest_framework.authtoken',
    'apps.dyn_datatables',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TWITTER_API_KEY='oepijMpavfqqqpsDE072Hb28B'
TWITTER_API_SECRET='P1Ya8CrzKfrZIBIol31HF66grNLSqCBunouFWQqWMqaO4uXqm4'
TWITTER_CLIENT_ID='bGFvU3FZUXpiV05HLTVpLVFIeTQ6MTpjaQ'
TWITTER_CLIENT_SECRET='07N81g_X_f-ktsBH92P6a2m4j_PYNp4bubp_Oj5hx7zmg4YRSI'
TWITTER_OAUTH_CALLBACK_URL='https://b225-42-105-82-248.in.ngrok.io/authorization/twitter_callback'

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.getenv('DB_NAME'     , 'appseed_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
        'HOST'    : os.getenv('DB_HOST'     , 'localhost'),
        'PORT'    : os.getenv('DB_PORT'     , 3306),
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
    os.path.join(BASE_DIR, "apps/dyn_datatables/templates/static"),
)

# This is used by the API Generator
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#############################################################
# OAuth settings 

GITHUB_ID     = os.getenv('GITHUB_ID', None)
GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)
GITHUB_AUTH   = GITHUB_SECRET is not None and GITHUB_ID is not None

AUTHENTICATION_BACKENDS = (
    "core.custom-auth-backend.CustomBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    'django.contrib.auth.backends.ModelBackend'
    

)

SITE_ID                    = 1 
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
        'APP': {
            'client_id': 'd5e31cb3df8e44146b89',
            'secret': '81783e908d9fa84788d31c023dba56b8e80544e9',
            'key': ''
        }
    },
    # 'twitter': {
    #     'APP': {
    #         'client_id':'bGFvU3FZUXpiV05HLTVpLVFIeTQ6MTpjaQ',
    #         'secret':'07N81g_X_f-ktsBH92P6a2m4j_PYNp4bubp_Oj5hx7zmg4YRSI',
    #         'key':'',
    #     }
    # }
}
# 'APP': {
        #     'client_id':'oepijMpavfqqqpsDE072Hb28B',
        #     'secret':'P1Ya8CrzKfrZIBIol31HF66grNLSqCBunouFWQqWMqaO4uXqm4',
        #     'key':'',
        # }

if GITHUB_AUTH:
    SOCIALACCOUNT_PROVIDERS['github'] = {
        'APP': {
            'client_id': 'd5e31cb3df8e44146b89',
            'secret': '81783e908d9fa84788d31c023dba56b8e80544e9',
            'key': ''
        }
    }


#############################################################
# API Generator

API_GENERATOR = {
    # Register models below
    'books': "Book",
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
}

#############################################################
# DYNAMIC DATA Tables

DYNAMIC_DATATB = {
    'endpoint': 'Model', # don't change this line

    # Register models below
    'books': "Book",     
}
YOUTUBE_DATA_API_KEY = 'AIzaSyDOyt6j4LpRxcGnA5ZBKcc2FYKUIvLnJzs'
