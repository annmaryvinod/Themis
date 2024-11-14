from typing import List

from pydantic import AnyHttpUrl, BaseModel, Field


class BaseConfig(BaseModel):
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    DATABASE_URL: str
    SECRET_KEY: str
    ALLOWED_HOSTS: List[AnyHttpUrl] = Field(default_factory=list)

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    HUGGINGFACEHUB_API_TOKEN: str

    model_config = {
        "env_prefix": "",  # No prefix by default
    }
