#!/bin/bash

# Wait for the DB (TODO)
sleep 5

echo "Apply database migrations"
python manage.py migrate

echo "Load fixtures"
python manage.py loaddata fixtures/*.json

echo "Starting server"
python manage.py runserver 0.0.0.0:8000
