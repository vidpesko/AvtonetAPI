import os
from pydantic_settings import BaseSettings, SettingsConfigDict


dotenv_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ".env")


class PostgresSettings(BaseSettings):
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5433
    postgres_database: str

    echo_sql: bool = True


class ProjectSettings(BaseSettings):
    project_name: str = "My FastAPI project"
    log_level: str = "DEBUG"


class Settings(ProjectSettings, PostgresSettings):
    model_config = SettingsConfigDict(env_file=dotenv_path, env_file_encoding="utf-8", extra="ignore")


settings = Settings()
