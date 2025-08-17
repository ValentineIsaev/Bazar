from bot.core.setup import configs, ConfigsName

print(configs)

PROJECT_ROOT = configs.get(ConfigsName.PROJECT_ROOT)
CACHE_MEDIA_DIR = configs.get(ConfigsName.CACHE_MEDIA_DIR)
