# """
# Django settings for car_auction project.

# Generated by 'django-admin startproject' using Django 5.1.6.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.1/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/5.1/ref/settings/
# """

# from pathlib import Path
# import os
# import pymysql


# pymysql.install_as_MySQLdb()


# INSTALLED_APPS += ["corsheaders"]

# MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

# CORS_ALLOW_ALL_ORIGINS = True  # Change to allowed frontend domains later



# # Base directory
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Security
# SECRET_KEY = 'django-insecure-^kv%z(5ix_$4hw)2fn=o48g6)09(7hv@ilmhppt%fasbo=i($v'
# DEBUG = True

# ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]


# # Installed apps
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Third-party apps
#     'rest_framework',
#     'channels',

#     # Local apps
#     'auctions',
#     'users',
# ]

# # Middleware
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # Root URL config
# ROOT_URLCONF = 'car_auction.urls'

# # Templates
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             BASE_DIR / "templates",  # Global templates folder
#             os.path.join(BASE_DIR, 'auctions', 'templates'),  # Auctions app templates
#         ],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# # ASGI application (for WebSockets)
# ASGI_APPLICATION = 'car_auction.asgi.application'
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     }
# }

# # Caching (optional for performance)
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# # ✅ Fixed MySQL Database Settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'cars_auction_db',
#         'USER': 'root',
#         'PASSWORD': '',  # Add your MySQL password if required
#         'HOST': '127.0.0.1',  # Change to 'localhost' if needed
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# # Authentication
# AUTH_USER_MODEL = 'auctions.User'
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ✅ Login & Logout Redirects
# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/dashboard/'  # Redirect after login
# LOGOUT_REDIRECT_URL = '/'  # Redirect after logout

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# # ✅ Media Files (User-uploaded images)
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# # ✅ Ensure media files are served in development mode
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     ...
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # ✅ MPesa Payment Integration (Ensure you update credentials)
# # M-Pesa API Credentials
# MPESA_BUSINESS_SHORTCODE = "174379"  # Sandbox shortcode
# MPESA_PASSKEY = "your_real_passkey_here"
# MPESA_CONSUMER_KEY = "LyfOVAO4qKqEWHXTIRO5adYxwGAK0KkhS1FgGPtGjIyllfsq"
# MPESA_CONSUMER_SECRET = "N4SoZwiX6ddSAjafrcduGLPQ5nnTJfVna03K3sLevbHpOgPLDAaQWWx4pBqAkucV"
# MPESA_CALLBACK_URL = "https://yourwebsite.com/payment/callback/"  # Replace with your real callback URL


# # ✅ Vehicle History API (Ensure you update API details)
# VEHICLE_HISTORY_API_URL = "https://api.example.com/vin/"
# VEHICLE_HISTORY_API_KEY = "your_api_key"





"""
Django settings for car_auction project.
"""

import os
from pathlib import Path
import pymysql
import dj_database_url
# ✅ Ensure media files are served in development mode
from django.conf import settings
from django.conf.urls.static import static

pymysql.install_as_MySQLdb()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-^kv%z(5ix_$4hw)2fn=o48g6)09(7hv@ilmhppt%fasbo=i($v")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".railway.app", ".onrender.com"]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'channels',
    'corsheaders',
    'django_redis',

    # Local apps
    'auctions',
    'users',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True  # Change to allowed frontend domains later

# Root URL config
ROOT_URLCONF = 'car_auction.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
            os.path.join(BASE_DIR, 'auctions', 'templates'),
        ],
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

# ASGI application (for WebSockets)
ASGI_APPLICATION = 'car_auction.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# ✅ Fixed Database Configuration (MySQL with dj-database-url)
DATABASES = {
    'default': dj_database_url.config(default='mysql://root:@127.0.0.1:3306/cars_auction_db', conn_max_age=600)
}


# Authentication
AUTH_USER_MODEL = 'auctions.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Login & Logout Redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirect after login
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files (Vercel doesn't serve static files directly)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")



urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Redis Caching (Optional, speeds up database queries)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ✅ MPesa Payment Integration (Ensure you update credentials)
# M-Pesa API Credentials
MPESA_BUSINESS_SHORTCODE = "174379"  # Sandbox shortcode
MPESA_PASSKEY = "your_real_passkey_here"
MPESA_CONSUMER_KEY = "LyfOVAO4qKqEWHXTIRO5adYxwGAK0KkhS1FgGPtGjIyllfsq"
MPESA_CONSUMER_SECRET = "N4SoZwiX6ddSAjafrcduGLPQ5nnTJfVna03K3sLevbHpOgPLDAaQWWx4pBqAkucV"
MPESA_CALLBACK_URL = "https://yourwebsite.com/payment/callback/"  # Replace with your real callback URL

# ✅ Vehicle History API (Ensure you update API details)
VEHICLE_HISTORY_API_URL = os.getenv("VEHICLE_HISTORY_API_URL", "https://api.example.com/vin/")
VEHICLE_HISTORY_API_KEY = os.getenv("VEHICLE_HISTORY_API_KEY", "your_api_key")

