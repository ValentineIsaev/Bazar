if pg_isready -q; then
  sudo service postgresql stop
fi

sudo service postgresql start &

source .venv/bin/activate
export PYTHONPATH="/home/valentine/PythonProject/Bazar:$PYTHONPATH"
python3 bot/main.py
