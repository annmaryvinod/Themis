import os

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

from app.config.base import BaseConfig


class Settings(BaseSettings, BaseConfig):
    ENV: str = Field(default="local", env="ENV")

    model_config = ConfigDict(
        env_file=[
            "configs/.env.base",
            f"configs/.env.{os.getenv('ENV', 'local')}",
        ],
        env_file_encoding="utf-8",
    )


settings = Settings()
