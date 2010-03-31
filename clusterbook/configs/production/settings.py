from clusterbook.configs.common.settings import *

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database
DATABASE_HOST = 'db.bar.example.com'
DATABASE_PORT = '5433'
DATABASE_USER = 'clusterbook'
DATABASE_PASSWORD = 'foo'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.bar.example.com/clusterbook/'

# Predefined domain
MY_SITE_DOMAIN = 'clusterbook.bar.example.com'

# Email
EMAIL_HOST = 'mail.tribapps.com'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# S3
AWS_S3_URL = 's3://media.bar.example.com/clusterbook/'

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)