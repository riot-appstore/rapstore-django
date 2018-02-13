Django and Docker Proof of Concept
==================================
# Description

This PoC currently) tries to use the current Python CGI script with Django and Docker. It covers:
* Django Rest Framework
* PostgreSQL
* Docker (with docker-compose)

# Dependencies
Install Docker and Docker-compose (sudo apt-get install docker python-pip docker-compose).

# Usage
Simply run `docker-compose -f install/docker-compose.yml up --build`. Docker compose will:
* Build a postgresql container
* Install Django, DRF and all dependencies
* Apply all DB migrations
* Serve the website at localhost:8000

If you want to populate the database with all examples, boards and modules, just execute (with the docker-compose up running!): `docker-compose -f install/docker-compose.yml exec web python manage.py populate_db`

# Admin
It's possible to add Boards, Modules and Applications directly from Django admin. Simply go to localhost:8000/admin.
Current config is:
* User: riot
* Pass: password0
