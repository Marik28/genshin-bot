from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DjangoLikeModel:
    class DoesNotExist(Exception):
        pass

    class AlreadyExists(Exception):
        pass


banner_and_character_association_table = Table(
    "banner_and_character_association", Base.metadata,
    Column('banner_id', ForeignKey('banners.id'), primary_key=True),
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
)


class Character(Base, DjangoLikeModel):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    rarity = Column(Integer, nullable=False)
    element = Column(String(15), nullable=False)
    weapon = Column(String(20), nullable=False)
    sex = Column(String(15), nullable=False)
    area = Column(String(20), nullable=False)


class CharacterImage(Base, DjangoLikeModel):
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    link = Column(String, nullable=False, unique=True)

    character = relationship(Character, backref="images")


class Banner(Base, DjangoLikeModel):
    __tablename__ = "banners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    characters = relationship(
        "Character",
        secondary=banner_and_character_association_table,
        backref="banners",
    )


class User(Base, DjangoLikeModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)


user_and_character_association_table = Table(
    "user_and_character_association", Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
)
