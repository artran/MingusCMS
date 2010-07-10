# Django settings for mingus project.
# See http://www.b-list.org/weblog/2007/nov/08/production/
import os

DIRNAME = os.path.dirname(__file__)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

ROOT_URLCONF = 'mingus.cms.urls'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)

# Workaround for PIL import issues.
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image

# Load the local settings
from local_settings import *
