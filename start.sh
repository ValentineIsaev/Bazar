#!/bin/bash

if pg_isready -q; then
  sudo service postgresql stop
fi

sudo service postgresql start &
sudo systemctl start redis-server

source .venv/bin/activate
export PYTHONPATH="/home/valentine/PythonProject/Bazar:$PYTHONPATH"
python3 bot/main.py
