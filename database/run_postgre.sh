#!/bin/bash

if ! command -v psql &> /dev/null; then
    source .env
    echo "PostgreSQL not install. Please, install PostgreSQL"
    exit 1
fi

if ! pg_isready -q; then
  echo 'Start server...'
  sudo service postgresql start
  echo 'Server start!'
fi