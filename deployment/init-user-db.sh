#!/bin/bash

# Create the database and user that the django app will use.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER recordlib
    CREATE USER recordlib
    GRANT ALL PRIVILEGES ON DATABASE recordlib TO recordlib