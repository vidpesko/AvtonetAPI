from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


cwd = Path.cwd()
dotenv_path = cwd / ".env"
if not list(cwd.glob(".env")):
    cwd = cwd.parent
    dotenv_path = cwd / ".env"

    if not list(cwd.glob(".env")):
        cwd = cwd.parent
        dotenv_path = cwd / ".env"


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

    def create_engine_url(self, async_driver: bool = False) -> str:
        """Generate engine url using pydantic_settings class

        Args:
            settings (Settings): Settings class

        Returns:
            str
        """

        return f"postgresql{"+asyncpg" if async_driver else ""}://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"


class ScraperSettings(BaseSettings):
    scraper_allowed_domains: list[str] = ["www.avto.net", "avto.net"]
    scraper_allowed_schemas: list[str] = [
        "https",
    ]

    # Maximum Vehicle entry age - maximum amount of time before Vehicle needs updating
    max_vehicle_age: int = 15  # In minutes

    # Shared
    vehicle_page_path_prefix: str = "/Ads/details.asp"

    # Car
    car_listing_page_spider_name: str = "vehicle"
    car_listings_spider_name: str = "vehicle_listing"

    # Motorcycle


class CelerySettings(BaseSettings):
    rabbitmq_broker_url: str = ""
    redis_backend_url: str = ""


class Settings(ProjectSettings, PostgresSettings, ScraperSettings, CelerySettings):
    model_config = SettingsConfigDict(
        env_file=str(dotenv_path), env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
