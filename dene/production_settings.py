import os

from dene.settings import *

DATABASES['default']['NAME'] = os.environ['DB_PATH']

DEBUG = False

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
