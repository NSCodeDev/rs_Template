#!/bin/bash

# collecting static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# run migrations
echo "Applying database migrations..."
python manage.py makemigrations --merge --noinput
python manage.py migrate

# run server 
echo "Starting server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8091 \
--worker-class gunicorn.workers.sync.SyncWorker \
--workers 3 \
--timeout 600