import sqlalchemy.orm
import typer
from sqlalchemy.exc import IntegrityError

from genshin_bot import tables, models


def insert_data(session: sqlalchemy.orm.Session, characters: list[models.Character]):
    with typer.progressbar(characters, label="Добавление персонажей в БД") as progress:
        for c in progress:
            character_to_add = tables.Character(
                name=c.name, rarity=c.rarity, weapon=c.weapon, element=c.element, sex=c.sex, area=c.area
            )
            image = tables.CharacterImage(link=str(c.images[0].link).strip())
            character_to_add.images.append(image)
            session.add(character_to_add)
            try:
                session.commit()
            except IntegrityError:
                typer.echo(f"{character_to_add.name} уже есть в БД")
                session.rollback()
