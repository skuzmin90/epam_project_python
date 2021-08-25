#!/bin/bash

export PGPASSWORD="$DB_PASSWORD"

psql -h "$DB_HOST" -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER';" | grep -q 1 || psql -h "$DB_HOST" -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -h "$DB_HOST" -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1 || psql -h "$DB_HOST" -U postgres -c "CREATE DATABASE $DB_NAME;"
psql -h "$DB_HOST" -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to $DB_USER;"