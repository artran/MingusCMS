from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

ADMINS = (
    ('Ray Tran', 'ray@artran.co.uk'),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

DIRNAME = os.path.dirname(__file__)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DIRNAME, 'mingus.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-gb'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'use ./manage.py generate_secret_key to generate the content'

INTERNAL_IPS = ('127.0.0.1', '192.168.0.74',)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.redirects',
    'django.contrib.humanize',
    'mingus.cms',
    'mingus.contact',
    'django_extensions',
    'django_nose',
    'south',
)

TEST_RUNNER = 'django_nose.run_tests'

CONTACT_RECIPIENTS = ('ray@artran.co.uk',)

REPO_ROOT = os.path.join(DIRNAME, 'repos')
