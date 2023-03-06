# JMDB

[![jmdb workflow](https://github.com/gavingreenhorn/jmdb/actions/workflows/jmdb_workflow.yml/badge.svg?event=push)](https://github.com/gavingreenhorn/jmdb/actions/workflows/jmdb_workflow.yml)

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

## Deploying the project to a remote machine with GitHub Actions workflow

First off, install [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) on your remote server using official guide (make sure that `Docker Compose` plugin is available as well). This is a prerequisite, so that GitHub Actions CI will be able to call Docker CLI.

Then you'll need to provide all configuration information in your repository secrets.
The following variables are expected:
- `HOST` = IP address of your remote server
- `USER` = your username on remote server
- `SSH_KEY` = private key that will be used to establish connection with your server (it should already know the public key)
- `PASSPHRASE` = only required if your SSH key is passphrase-protected (you'll also need to uncomment the setting in workflow file)
- `DOCKER_USERNAME` = your Docker Hub username (the project is going to be made into a docker image and pushed to Docker Hub)
- `DOCKER_USERNAME` = your Docker Hub password
- `DB_ENGINE` = database backend that is going to be used by the project. Default: 'django.db.backends.postgresql'
- `DB_HOST` = should be equal to the name of DB container in a docker-compose file. Default: jmdb_db
- `DB_PORT` = port at which DB service is going to listen. Default: 5432
- `DB_NAME` = database that's going to be created on DB container's deployment. Default: postgres
- `DB_USER` = username of a user that's going to be created on deployment.
- `DB_PASSWORD` = this user's password.  
*These are passed to the DB container's environment as POSTGRES_USER and POSTGRES_PASSWORD variables. If you're going to replace DB backend, make sure to change ENV variables in the worflow according to the requirements of new backend*
- `SECRET` = Django's SECRET_KEY
- `SU_NAME` = Django Superuser account created on deployment
- `SU_EMAIL` = its email
- `SU_PASSWORD` = its password
- `EMAIL_ADDRESS` = address of a mailbox that is going to be used to send out registration information to new users
- `EMAIL_USER` = account name of the mailbox owner
- `EMAIL_PASSWORD` = password to that account
- `TELEGRAM_TOKEN` = *optional* Token for you Telegram bot that will send out notifications about successful deployment
- `TELEGRAM_TO` = *optional* Chat ID to which notifications are going to be sent

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
