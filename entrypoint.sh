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
python manage.py runserver 0.0.0.0:${PORT}