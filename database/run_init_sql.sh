#!/bin/bash

sudo -u postgres psql -v db_user="$DB_USER" \
     -v user_password="$PASSWORD" \
     -v db_name="$DB_NAME"
     -d $DB_NAME -f 'init.sql'