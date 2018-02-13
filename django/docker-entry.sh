#!/bin/bash

# Wait for the DB (TODO)
sleep 5
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Load fixtures
echo "Apply database migrations"
python manage.py loaddata fixtures/*

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
