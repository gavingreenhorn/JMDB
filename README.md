# JMDB

[![jmdb workflow](https://github.com/gavingreenhorn/jmdb_final/actions/workflows/jmdb_workflow.yml/badge.svg?event=push)](https://github.com/gavingreenhorn/jmdb_final/actions/workflows/jmdb_workflow.yml)

## Summary

The project exposes an API that allows users to read and score various works, leave reviews and comment on other users reviews.
The project is deployed to three separate Docker containers, of which:  
- **jmdb_web** is hosting a Django application that exposes REST API via Django Rest Framework.
- **jmdb_db** is hosting a Postgres database
- **jmdb_nginx** is hosting an NGINX web-server. The web-server interfaces with Django WSGI app via gunicorn.

## Contents

1. [Deploying the project locally](#Deploying-the-project-locally)
2. [Registration](#Registration)
3. [Roles](#Roles)
4. [Resources](#Resources)

## Deploying the project locally

```
git clone https://github.com/gavingreenhorn/jmdb
cd ~/jmdb
docker compose -f infra/docker-compose.yaml up
docker cp api_jmdb/static/. web:/app/static/
docker exec jmdb_web python manage.py makemigrations reviews users auth_jmdb
docker exec jmdb_web python manage.py migrate [--verbosity { 1 | 2 | 3 }]
docker exec jmdb_web python manage.py collectstatic --no-input
```
The Project creates models and fills database with dummy data from csv-files in the directory **/app/static/data** of container **jmdb_web**

Ad hoc database fill is available using a JSON dump and a built-in Django command below (run from the project's root directory):
```
python api_jmdb/manage.py loaddata dbdump.json
```

Expected environment variables (the project would read .env file from ./infra directory):
- **DB_NAME** - database name (db container creates a default db 'postgres' on deployment, so you can use this name, unless you want to create a new one manually)
- **DB_HOST** - container hosting a db (docker compose file specifies 'jmdb_db')
- **DB_PORT** - port on which postrges service is listening (5432 by default)
- **POSTGRES_USER** - DB user name
- **POSTGRES_PASSWORD** - DB user password
- **EMAIL_PASSWORD** - password that the project backend will use for registration
- **EMAIL_USER** - email login name
- **EMAIL_ADDRESS** - email used for sending confirmation code
- **NGINX_HOST** - IP address that will host web server (127.0.0.1 if deploying locally)
- **SECRET** - Django's SECRET_KEY

## Deploying the project to a remote machine

First off, install [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) on your remote server using official guide (make sure that `Docker Compose` plugin is available as well). This is a prerequisite, so that GitHub Actions CI will be able to call Docker CLI.

## Registration

1. User sends a POST request with parameters `email` и `username` to the endpoint `/api/v1/auth/signup/`
2. New user if all fields are validates and email was successfully dispatched
3. **jmdb** add sends a code (`confirmation_code`) to the specified address (`email`)
4. User send a POST request with parameters `username` and `confirmation_code` to the endpoint `/api/v1/auth/token/` and receives a `token` (JWT) with successful response
5. Going forward, user might send a PATCH request to the endpoint `/api/v1/users/me/` and fill optional fields in his profile

## Roles

- **Anonimous** — can view titles, reviews and comments.
- **Authenticated user** — can publish reviews, score works, and comment on reviews; can edit and delete his reviews and comments, can change his scores. Default role.
- **Moderator** — Everything above, plus can delete or edit any review or comment.
- **Admin** — Everything above, plus the rights to create and delete works, categories and genres. Can assign roles to users.
- **Superuser** - Has all the rights regardless of roles.

> Django admin panel is available at `/admin/`

## Resources

- **auth**: authentication
- **users**: users
- **titles**: works
- **categories**: categories of works (film, book, song)
- **genres**: genres of works. Each work can belong to multiple genres
- **reviews**: reviews to works
- **comments**: comments to reviews

## API documentation

Is generated automatically according to OpenAPI standard and available on the endpoints:  
>`/swagger/`  
`/redoc/`

[:arrow_up:Contents](#Contents)
