from app.config import Settings


def create_engine_url(settings: Settings) -> str:
    """Generate engine url using pydantic_settings class

    Args:
        settings (Settings): Settings class

    Returns:
        str
    """

    return f"postgresql+asyncpg://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
