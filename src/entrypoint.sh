#!/bin/sh

while ! nc -z db 5432; do
  sleep 0.1
done

python movie_library/manage.py flush --no-input
python movie_library/manage.py makemigrations
python movie_library/manage.py migrate
python movie_library/manage.py collectstatic --noinput
exec "$@"