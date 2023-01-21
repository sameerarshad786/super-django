#!/bin/bash

cd ../../
python3.8 -m venv venv
source venv/bin/activate
pip install -r super_social/requirements.txt

POSTGRES_VERSION=$(psql --version)

if ! [[ $POSTGRES_VERSION ]]
then
    echo "You don't have postgres installed on your system"
    pip install postgres
fi

PSQL="psql -X --dbname=postgres -w postgres --no-align --tuples-only -c"
ENTER_TO_PSQL=$($PSQL "CREATE DATABASE paksocial;")
echo -e "\n\n Project Succesfully Setup\n\n"
