from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    discord_api_token: str
    command_prefix: str = "."

    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 1

    debug: bool = False
    flask_secret_key: str
    admin_app_host: str = 'localhost'
    admin_app_port: int = 5001
    basic_auth_username: str
    basic_auth_password: str
    admin_url: str = "/genshin/admin/"

    characters_url: str = "https://genshin-impact.fandom.com" \
                          "/ru/wiki/%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8"
    genshin_wiki_base_url: str = "https://genshin-impact.fandom.com"

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    database_url: str = f"sqlite:///{base_dir / 'db.sqlite3'}"


settings = Settings()

if not settings.base_dir.exists():
    settings.base_dir.mkdir()
