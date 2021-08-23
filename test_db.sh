#!/bin/bash
apt-get install --yes --no-install-recommends postgresql-client

CREATE USER ${{ secrets.TEST_DB_USER }} WITH PASSWORD ${{ secrets.TEST_DB_PASSWORD }};
CREATE DATABASE ${{ secrets.TEST_DB_NAME }};
GRANT ALL PRIVILEGES ON DATABASE ${{ secrets.TEST_DB_NAME }} to ${{ secrets.TEST_DB_USER }};
