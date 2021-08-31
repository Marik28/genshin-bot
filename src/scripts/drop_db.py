from loguru import logger
from sqlalchemy_utils.functions import drop_database, database_exists

from genshin_bot.database import engine

if __name__ == '__main__':
    db_url = engine.url
    logger.debug(f"БД - {db_url}")
    if database_exists(db_url):
        drop_database(db_url)
        logger.warning(f"БД {db_url} удалена")
    else:
        logger.warning("Такой БД не существует")
