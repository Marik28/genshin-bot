import argparse
import json

import sqlalchemy.orm
from loguru import logger
from sqlalchemy.exc import IntegrityError

from genshin_bot import tables, models
from genshin_bot.database import Session
from genshin_bot.settings import settings

parser = argparse.ArgumentParser()
parser.add_argument(
    "filename",
    help="Имя json файла со списком персонажей. Файл должен лежать в папке data/json в корне проекта"
)
json_dir = settings.base_dir / "data" / "json"
if not json_dir.exists():
    json_dir.mkdir()


def insert_data(filename, session: sqlalchemy.orm.Session):
    with open(json_dir / filename) as f:
        character_obj_list = json.load(f)
    characters: list[models.Character] = [models.Character.parse_obj(character_obj) for character_obj in
                                          character_obj_list]
    for c in characters:
        character_to_add = tables.Character(name=c.name, rarity=c.rarity, weapon=c.weapon, element=c.element,
                                            sex=c.sex, area=c.area)
        image = tables.CharacterImage(link=str(c.images[0].link).strip())
        logger.debug(f"{character_to_add.name} - {image}")
        character_to_add.images.append(image)
        logger.info(f"Добавляю {character_to_add.name}")
        session.add(character_to_add)
        try:
            session.commit()
        except IntegrityError:
            logger.warning(f"{character_to_add.name} уже есть в БД")
            session.rollback()


def add_default_banner(session: sqlalchemy.orm.Session):
    default_banner_name = "Default"
    default_banner = tables.Banner(name=default_banner_name)
    session.add(default_banner)
    all_characters = session.query(tables.Character).all()
    default_banner.characters.extend(all_characters)
    session.add(default_banner)
    session.commit()
    logger.info(f"Создан дефолтный баннер {default_banner.name} и в него добавлены все персонажи")


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    with Session() as session:
        insert_data(filename, session)
        add_default_banner(session)
