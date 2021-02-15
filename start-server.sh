#!/usr/bin/env bash

if [ -n "$ALLOWED_HOSTS" ]; then
  sed -i "s/ALLOWED_HOSTS =.*/ALLOWED_HOSTS = \['$ALLOWED_HOSTS'\]/" dene/production_settings.py
  export DJANGO_SETTINGS_MODULE="dene.production_settings"
else
  export DJANGO_SETTINGS_MODULE="dene.settings"
fi

if [ -n "$SECRET_KEY" ]; then
  export SECRET_KEY="$SECRET_KEY"
else
  export SECRET_KEY="51%5^189l7c)q7*m970xawkd5k-bq2dh&92j4&&tuuzg&t5p2b"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

chown www-data:www-data /opt/app/dene/db.sqlite3

# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(gunicorn dene.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"