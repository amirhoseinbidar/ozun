"""
Django settings for ozun project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import json
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(BASE_DIR+'/env_var.json','r') as file:
    ENV = json.loads(file.read())
    

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


SECRET_KEY =  ENV['SECRET_KEY']  
DEBUG = ENV['DEBUG']
ALLOWED_HOSTS = ENV['ALLOWED_HOSTS'].split(',')



# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

EXTRA_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_cleanup',
    'treebeard',
    'taggit',
    'rest_auth',
    'django_webtest',
    #'ckeditor'
    
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
]

LOCAL_APPS = [
    'core',
    'quizzes',
    'users',
    'restAPI',
    'studypost',
    'qa',
    'markdownx',
]

INSTALLED_APPS = DJANGO_APPS + EXTRA_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ozun.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+'/template', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # `allauth` needs this from django
                'django.template.context_processors.request',
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

WSGI_APPLICATION = 'ozun.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if ENV['UNDER_TEST']:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }   
    }
else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': ENV['DB_NAME'],
            'USER': ENV['DB_USER'],
            'PASSWORD': ENV['DB_PASSWORD'],
            'HOST': ENV['DB_HOST'] ,
            'default-character-set': ENV['DB_CHARSET'],
        },
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)
STATICFILES_FINDER = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.appDirectoriesFinder',
]
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

##### Media Files #####

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'


##### Email setting #####
if ENV['REAL_SERVER']:
    EMAIL_USE_TLS = True
    EMAIL_HOST = ENV['EMAIL_HOST']
    EMAIL_HOST_USER = ENV['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD =  ENV['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = 587

##### Rest framework authentication setting #####
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# this make life easier
if not ENV['REAL_SERVER']:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'rest_framework.authentication.SessionAuthentication'
    )

##### allauth setting #####
ACCOUNT_USERNAME_MIN_LENGTH = 6
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'


##### allauth rest setting #####
SITE_ID = 1
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'restAPI.serializers.UserSerializer'
}

##### ozun setting #####
DIFAULT_SEND_QUIZ = 7
