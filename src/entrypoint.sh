#!/bin/sh

while ! nc -z db 5432; do
  sleep 0.1
done

python movies/manage.py flush --no-input
python movies/manage.py migrate
python movies/manage.py collectstatic --noinput
exec "$@"