from clusterbook.configs.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5433'
DATABASE_USER = 'clusterbook'
DATABASE_PASSWORD = 'foo'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://clusterbook.s3.amazonaws.com/'

# Predefined domain
MY_SITE_DOMAIN = 'clusterbook.foo.example.com'

# Email
EMAIL_HOST = 'mail.foo.example.com'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# S3
AWS_S3_URL = 's3://clusterbook/'


GOOGLE_MAPS_API_KEY = "ABQIAAAA8E1c1-rPGKc2CBMpfB181RSTZLRs7D-Z-pQY-iUlzqRzHZ3ibRQ9BpQaTIeKZQgDsAxGDvNNK3omzw" # for all 'amazonaws.com'


# Trib IPs for security
INTERNAL_IPS = ()

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)