from pathlib import Path
import os
import shutil

from bot.utils.exception import EmptyConfig

from dotenv import load_dotenv
from aiogram import Bot


class ConfigsName:
    PROJECT_ROOT = 'PROJECT_ROOT'

    BOT_TOKEN = 'BOT_TOKEN'

    CACHE_DIR = 'CACHE_DIR'
    CACHE_MEDIA_DIR = 'CACHE_MEDIA_DIR'

PROJECT_ROOT = Path(__file__).parent.parent
configs: dict = {ConfigsName.PROJECT_ROOT: PROJECT_ROOT}


def clear_cache(cache_dir: Path):
    for d in cache_dir.rglob('*'):
        print(d, d.parent)
        if d.is_dir() and d.parent != cache_dir:
            shutil.rmtree(d)


def _load_config(key: str) -> str:
    config = os.getenv(key)
    if config is None:
        raise EmptyConfig(key)
    return config


def load_config() -> dict:
    global configs

    env_file = PROJECT_ROOT / '.env'
    if not env_file.exists():
        raise ValueError(f'Env file not exist or is not locates at {env_file}')
    load_dotenv(env_file)

    bot_token = _load_config(ConfigsName.BOT_TOKEN)
    configs[ConfigsName.BOT_TOKEN] = bot_token

    cache_dir = Path(_load_config(ConfigsName.CACHE_DIR))
    configs[ConfigsName.CACHE_DIR] = cache_dir

    media_cache_dir = Path(_load_config(ConfigsName.CACHE_MEDIA_DIR))
    if media_cache_dir.parent != cache_dir:
        raise ValueError(f'Media cache dir need heir cache dir: {cache_dir}. Your cache dir: {media_cache_dir}')
    configs[ConfigsName.CACHE_MEDIA_DIR] = media_cache_dir

    return configs


def setup() -> Bot:
    load_configs = load_config()
    clear_cache(load_configs.get(ConfigsName.CACHE_DIR))
    bot = Bot(load_configs.get(ConfigsName.BOT_TOKEN))

    return bot
