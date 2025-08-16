#!/bin/bash

if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not install. Please, install PostgreSQL"
    exit 1
fi

if ! pg_isready -q; then
  echo 'Start server...'
  sudo service postgresql start
  echo 'Server start! Run init...'

  if [ -f .env ]; then
    source .env
  else
    echo '.env do not exist!'
    exit 1
  fi

  PART1="Variable"
  PART2="is empty or not specified."
  check_var() {
      local var_name=$1
      if [[ ! -v ${var_name} ]] || [[ -z "${!var_name}" ]]; then
          echo "$PART1 $var_name $PART2"
          exit 1
      fi
  }

  check_var DB_NAME
  check_var PASSWORD
  check_var DB_USER

  if ! [ -f init.sql ]; then
    echo "File init.sql do not exist"

  sudo -u postgres psql -v db_user="$DB_USER" \
   -v user_password="$PASSWORD" \
   -v db_name="$DB_NAME"
   -d postgres -f 'init.sql'
fi