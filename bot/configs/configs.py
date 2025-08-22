from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, SecretStr

from pathlib import Path

from bot.utils.exception import LoadConfigError


ENV_PATH = Path(__file__).parent.parent.parent / '.env'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore')


class BotConfigs(ConfigBase):
    BOT_TOKEN: SecretStr = Field(..., min_length=46, max_length=46)


class DataBaseConfigs(ConfigBase):
    DATABASE_URL: SecretStr


class CacheConfigs(ConfigBase):
    CACHE_DIR: Path
    CACHE_MEDIA_DIR: Path

    @field_validator('CACHE_DIR')
    def check_cache_dir(cls, cache_dir: Path):
        if not cache_dir.exists():
            raise LoadConfigError('Cache dir is not exits!')
        return cache_dir

    @field_validator('CACHE_MEDIA_DIR')
    def check_cache_media_dir(cls, media_cache_dir: Path, info):
        cache_dir = info.data.get('CACHE_DIR')

        if not media_cache_dir.exists():
            raise LoadConfigError('Cache dir is not exits!')
        if media_cache_dir.parent != cache_dir:
            raise LoadConfigError(
                f'Media cache dir need heir cache dir: {cache_dir}. Your cache dir: {media_cache_dir}')
        return media_cache_dir


bot_configs = BotConfigs()
db_configs = DataBaseConfigs()
cache_configs = CacheConfigs()
