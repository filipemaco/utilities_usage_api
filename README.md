# API for Utilities Usage

## Available Scripts
In the project directory, you can run:

### How to run?
- Run `make` or `docker-compose up --build`

### How to makemigrations and migrate?
- Run `docker-compose exec utilities_api python manage.py makemigrations`
- Run `docker-compose exec utilities_api python manage.py migrate`

### How to run tests?
- Run `docker-compose exec utilities_api python manage.py test`

### How to run coverage and get report?
- Run `docker-compose exec utilities_api coverage run manage.py test -v 2`
- Run `docker-compose exec utilities_api coverage report -m`

- Coverage Result: 99%

### How to enter in container?
- Run `docker exec -it utilities-service-api /bin/sh`

### How to see the documentation?
- The documentation is available in `openapi.yml`
- You can copy the documentation to this link: https://editor.swagger.io/
- To make all the requests, except login, is necessary to add in `Headers` the `Authorization: Bearer token`.

### How to create the documentation?
- Enter in the container and run the following command: `python manage.py generateschema > openapi-schema.yml`

### How to create superuser?
- Run `docker-compose exec utilities_api python manage.py createsuperuser`

### Available users
Email | Password | SuperUser
------------ | ------------- | -------------
admin@example.com | admin | True
filipe@test.com | Password | False
jose@test.com | Password | False
miguel@test.com | Password | False

#### Documentation of important libraries used in this project
- Django: https://www.djangoproject.com/
- djangorestframework: https://www.django-rest-framework.org/
- dj-rest-auth: https://dj-rest-auth.readthedocs.io/en/latest/
- django-filter: https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
