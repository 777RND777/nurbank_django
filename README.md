# This is an API for NurBank database.
NurBank is a fictional bank for loans.

## Normal run:
1. Run migrations.
    ```shell
    python api/manage.py migrate
    ```
2. Run server.
    ```shell
    python api/manage.py runserver
    ```

## Run using docker-compose.
1. Create requirements.txt from pipenv.
    ```shell
    pipenv run pip freeze > requirements.txt
    ```
2. Run docker-compose.
    ```shell
    docker-compose up
    ```
3. Exec into api container and run migrations.
    ```shell
    docker exec -it CONTAINER_ID /bin/bash
    python manage.py migrate
    ```
