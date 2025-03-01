from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-veauul-*h^928+2^jqbby4((e^a(qf(eypra01#$--8z)&+d^u'

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ✅ **Application Definition**
INSTALLED_APPS = [
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',  # Django REST Framework
    'corsheaders',  # Enables CORS for frontend integration

    # ✅ **Custom Apps**
    'inventory',  # Inventory Management App
    'reports',  # ✅ New Reports Module
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Allow Cross-Origin Requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Ensure this points to "templates/"
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

WSGI_APPLICATION = 'inventory_project.wsgi.application'

# ✅ **Database Configuration (SQLite or PostgreSQL)**
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),  # ✅ Ensuring String Format
    }
}

# ✅ **Uncomment for PostgreSQL**
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'inventory_db',  # Change to your database name
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

# ✅ **Password Validation**
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ **Internationalization**
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Pacific/Port_Moresby'  # ✅ Corrected Timezone for PNG (GMT+10)
USE_I18N = True
USE_TZ = True

# ✅ **Static Files**
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# ✅ **Default Primary Key Field Type**
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ **Django REST Framework Settings**
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ✅ **JWT Authentication Settings**
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ✅ **CORS Configuration (Allow Frontend Requests)**
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (Use only for development)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React Frontend
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
