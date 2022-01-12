import argparse
import json

from sqlalchemy.exc import IntegrityError

from genshin_bot import tables, models
from genshin_bot.database import Session
from genshin_bot.settings import settings

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Имя json файла со списком персонажей")
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
    file = args.file
    insert_data(file)
