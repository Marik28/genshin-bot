from loguru import logger
from sqlalchemy_utils.functions import database_exists, create_database

from genshin_bot.database import engine

if __name__ == '__main__':
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("База данных создана")
    else:
        logger.info("База данных уже существует")
