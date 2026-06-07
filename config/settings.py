from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    smtp_host: str = Field(default="smtp.office365.com")
    smtp_port: int = Field(default=587)
    smtp_user: str = Field(default="")
    smtp_password: str = Field(default="")

    default_group: str = Field(default="it-team")
    escalation_group: str = Field(default="management")

    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000)
    api_key: str = Field(default="")

    log_file: str = Field(default="logs/audit.log")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
