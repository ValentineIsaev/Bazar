import os
from dotenv import load_dotenv
from pathlib import Path

from bot.utils.exception import EmptyConfig

PROJECT_ROOT = Path(__file__).parent.parent

load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

def load_config(key: str): # Нуждается в переписывании
    config = os.getenv(key)
    if config is None:
        raise EmptyConfig(key)
    return config

TOKEN = load_config('BOT_TOKEN')
MEDIA_CACHE_DIR = load_config('CACHE_MEDIA_DIR')
