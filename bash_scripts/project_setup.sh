#!/bin/bash

cd ../../
python3.8 -m venv venv
source venv/bin/activate
cd super-social/
pip install -r requirements.txt

POSTGRES_VERSION=$(psql --version)

if ! [[ $POSTGRES_VERSION ]]
then
    echo -e "\n\n~~~ You don't have postgres installed on your system ~~~\n\n"
    sudo apt update
    sudo apt install postgresql
fi

PSQL="psql -X --dbname=postgres --no-align --tuples-only -c"
ENTER_TO_PSQL=$($PSQL "CREATE DATABASE super_social;")

python manage.py migrate

echo -e "\n\n Project Succesfully Setup\n\n"
