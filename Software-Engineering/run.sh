#!/usr/bin/env sh

echo "Starting the server..."

python3 -m pip install -r requirements.txt

python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:80
