import os
from pydantic_settings import BaseSettings, SettingsConfigDict


dotenv_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), ".env")


class ProjectSettings(BaseSettings):
    project_name: str = "My FastAPI project"
    log_level: str = "DEBUG"


class PostgresSettings(BaseSettings):
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5433
    postgres_database: str

    echo_sql: bool = False


class ScraperSettings(BaseSettings):
    scraper_allowed_domains: list[str] = ["www.avto.net", "avto.net"]
    scraper_allowed_schemas: list[str] = ["https", ]

    # Maximum Vehicle entry age - maximum amount of time before Vehicle needs updating
    max_vehicle_age: int = 15  # In minutes

    vehicle_page_spider_name: str = "vehicle"
    vehicle_listing_spider_name: str = "vehicle_listing"
    vehicle_page_path_prefix: str = "/Ads/details.asp"


class CelerySettings(BaseSettings):
    rabbitmq_broker_url: str = ""
    redis_backend_url: str = ""


class Settings(ProjectSettings, PostgresSettings, ScraperSettings, CelerySettings):
    model_config = SettingsConfigDict(env_file=dotenv_path, env_file_encoding="utf-8", extra="ignore")


settings = Settings()
