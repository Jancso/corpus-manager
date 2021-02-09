import os

from dene.settings import *

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = ['.corpus-manager.ch']

#CSRF_COOKIE_SECURE = True

#SESSION_COOKIE_SECURE = True
