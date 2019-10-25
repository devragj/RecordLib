#!/bin/bash

# Create the database and user that the django app will use.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --set=rlpass="$RECORDLIB_DB_PW" <<-EOSQL
    CREATE USER recordlib;
    CREATE DATABASE recordlib;
    GRANT ALL PRIVILEGES ON DATABASE recordlib TO recordlib;
    ALTER USER recordlib WITH PASSWORD :'rlpass';