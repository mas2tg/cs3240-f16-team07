"""
Django settings for safecollab project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DATABASE_PATH = os.path.join(PROJECT_PATH, 'safecollab.db')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9e=qr&gq)jdg2_=p8=$y@$ro*6b)s-qp*i3xzgsb+3pn2=ih1)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'social.apps.django_app.default',
    'crispy_forms',
    'safecollab',
    'users',
    'reports',
    'inbox',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.ForceLogoutMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'safecollab.urls'
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/home'

WSGI_APPLICATION = 'safecollab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
    	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'safecollab',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
	'django.contrib.auth.hashers.BCryptPasswordHasher',
	'django.contrib.auth.hashers.PBKDF2PasswordHasher',
	'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Absolute path to the media directory

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,first_name,last_name,email', 
}

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'online',
    'approval_prompt': 'auto',
}

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # # Make up a username for this person, appends a random string at the end if
    # # there's any collision.
    # 'social.pipeline.user.get_username',

    # # Send a validation email to the user to verify its email address.
    # # Disabled by default.
    # # 'social.pipeline.mail.mail_validation',

    # # Associates the current social details with another user account with
    # # a similar email address. Disabled by default.
    # # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    # 'social.pipeline.user.create_user',
    'users.pipeline.get_additional_user_info',
    'users.pipeline.create_user',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # # Update the user record with any changed info from the auth service.
    # 'social.pipeline.user.user_details',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1717485655201998'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a022503ae502a0b6e30569c17626481d'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '337812304331-sn0h5i0corv70kaunh7dp5dfm41jr4aq.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'W_R4oR0HH9h-TtzTa43YCng2'
SOCIAL_AUTH_TWITTER_KEY = 'qmEgGpPCX5FsAkzSIyv7aKZ2e'
SOCIAL_AUTH_TWITTER_SECRET = 'XR3hSZ0NpA1MNlP2NOMNtlSxobupqWLR6ZIA2TdFm62QcPno0m'


    
CRISPY_TEMPLATE_PACK = 'bootstrap3'










