Django and Docker Proof of Concept
==================================
# Description

This PoC tries to use the current Python CGI script with Django and Docker. It covers:
* Django Rest Framework
* PostgreSQL
* Docker (with docker-compose)

# Install
Install Docker and Docker-compose (sudo apt-get install docker python-pip docker-compose).

Then, simply run `docker-compose up --build`. Docker compose will:
* Build a postgresql container
* Install Django, DRF and all dependencies
* Apply all DB migrations
* Serve the website at localhost:8000

# How to use
* After serving the website, go to localhost:8000.

# Extending
* Add more models in api/models.py.
* Add serializers for a model in api/serializers.py
* Add a view for that serializer in api/views.py
* Add an entry in riot_apps/settings.py
* Last but not least, generate migrations file (since new models make changes in DB) with: `docker-compose run web python manage.py makemigrations`
* Then, run `docker-compose up --build` again.

