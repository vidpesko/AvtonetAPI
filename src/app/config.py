from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5433
    postgres_database: str


class ProjectSettings(BaseSettings):
    project_name: str = "My FastAPI project"
    log_level: str = "DEBUG"


class Settings(ProjectSettings, PostgresSettings):
    pass

settings = Settings()  # type: ignore
