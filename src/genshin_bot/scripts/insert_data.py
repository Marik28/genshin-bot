import argparse
import json

from loguru import logger
from sqlalchemy.exc import IntegrityError

from .. import tables, models
from ..database import Session
from ..settings import settings

parser = argparse.ArgumentParser()
parser.add_argument(
    "filename",
    help="Имя json файла со списком персонажей. Файл должен лежать в папке data/json в корне проекта"
)
json_dir = settings.base_dir / "data" / "json"


def insert_data(filename):
    with open(json_dir / filename) as f:
        character_obj_list = json.load(f)
    with Session() as session:
        characters: list[models.Character] = [models.Character.parse_obj(character_obj) for character_obj in
                                              character_obj_list]
        for c in characters:
            character_to_add = tables.Character(name=c.name, rarity=c.rarity, weapon=c.weapon, element=c.element,
                                                sex=c.sex, area=c.area)
            image = tables.CharacterImage(link=str(c.images[0].link).strip())
            logger.debug(f"{character_to_add.name} - {image}")
            character_to_add.images.append(image)
            print(f"Добавляю {character_to_add.name}")
            session.add(character_to_add)
            try:
                session.commit()
            except IntegrityError:
                print(f"{character_to_add.name} уже есть в БД")
                session.rollback()


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    insert_data(filename)
