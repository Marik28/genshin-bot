from loguru import logger
from sqlalchemy_utils.functions import database_exists, create_database

from genshin_bot.database import engine
from genshin_bot.tables import Base

if __name__ == '__main__':
    db_url = engine.url
    if not database_exists(db_url):
        create_database(db_url)
        Base.metadata.create_all(engine)
        logger.info(f"База данных {db_url} создана")
    else:
        logger.info(f"База данных {db_url} уже существует")
