#!/bin/bash

if pg_isready -q; then
  sudo service postgresql stop
  echo 'Sever stop!'
fi