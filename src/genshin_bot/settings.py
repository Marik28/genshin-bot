from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    discord_api_token: str
    command_prefix: str = "."

    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 1

    database_url: str = "sqlite:////home/mark/PycharmProjects/genshin-bot/db.sqlite3"

    base_dir: Path = Path('/home/mark/PycharmProjects/genshin-bot/')


settings = Settings()
