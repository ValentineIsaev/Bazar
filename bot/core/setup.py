from pathlib import Path
import shutil

from bot.configs.configs import cache_configs, bot_configs

from aiogram import Bot


def clear_cache(cache_dir: Path):
    for d in cache_dir.rglob('*'):
        print(d, d.parent)
        if d.is_dir() and d.parent != cache_dir:
            shutil.rmtree(d)


def setup() -> Bot:
    clear_cache(cache_configs.CACHE_DIR)
    bot = Bot(bot_configs.BOT_TOKEN.get_secret_value())

    return bot
