# Django settings for babylab_project project.
import os

#set to false when running in production!
DEBUG = True

ADMINS = [
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '', #name of database [REQUIRED]
        # The following settings are not used with sqlite3:
        'USER': '', #postgresql user who has access to the database [REQUIRED]
        'PASSWORD': '', #password for above user [REQUIRED]
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# change this value when used on a different server
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

TIME_INPUT_FORMATS = ['%I:%M %p', '%I:%M%p', '%H:%M']

DATE_INPUT_FORMATS = ['%m-%d-%Y',]

DATETIME_INPUT_FORMATS = [
    '%m-%d-%Y %I:%M %p',      # '10-25-2006 02:30 PM'
#    '%Y-%m-%d %I:%M%p',      # '2006-10-25 02:30PM'
#    '%Y-%m-%d %I:%M %p',     # '2006-10-25 02:30 PM'
#    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
#    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
#    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
#    '%Y-%m-%d',              # '2006-10-25'
#    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
#    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
#    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
#    '%m/%d/%Y',              # '10/25/2006'
#    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
#    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
#    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
#    '%m/%d/%y',              # '10/25/06'
]

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Adding base directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/var/www/html/static'
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Make this unique, and don't share it with anybody.
# here's a site that can generate them if you don't want to generate your own: 
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '' # [REQUIRED]

#new format for templates starting in Django 1.8
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        os.path.join(BASE_DIR, 'templates'),
        #'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request' #added for django_tables2
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.WhodidMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ROOT_URLCONF = 'babylab_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'babylab_project.wsgi.application' 

AUTH_USER_MODEL = 'core.MyUser'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'crispy_forms',
    'people',
    'study',
    'scheduling',
    'localflavor',
    'django_tables2',
    'core',
    'pytz',
    'django_extensions',
    # 'debug_toolbar',
    'rest_framework'
]

INTERNAL_IPS = ["127.0.0.1",]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s'
        },
    },
    'handlers': {
       'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '', #location of where to save log file [REQUIRED IF USING LOGGING], e.g. '/home/username/babylab_project/babylab_project/babylab.log'
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'babylab_project': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

#other things needed to run this in production
#currently don't have https for the server, so ignoring these
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
