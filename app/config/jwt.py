from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from .environment import env_config


class JWTConfig(BaseSettings):
    """데이터베이스 설정"""
    ALGORITHM: str
    ACCESS: str
    ACCESS_KEY: str
    ACCESS_EXPIRED_AT: int
    REFRESH: str
    REFRESH_KEY: str
    REFRESH_EXPIRED_AT: int

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix='JWT_',
        env_file=env_config.env_file,
        extra='ignore'
    )