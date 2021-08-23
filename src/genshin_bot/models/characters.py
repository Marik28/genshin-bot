from enum import Enum
from enum import IntEnum

from pydantic import BaseModel


class Weapon(str, Enum):
    SWORD = "Меч"
    CATALYST = "Катализатор"
    CLAYMORE = "Двуручный меч"
    BOW = "Лук"
    POLEARM = "Копьё"


class Sex(str, Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class Rarity(IntEnum):
    THREE = 3
    FOUR = 4
    FIVE = 5


class Element(str, Enum):
    GEO = "Гео"
    PYRO = "Пиро"
    HYDRO = "Гидро"
    ELECTRO = "Электро"
    CRYO = "Крио"
    ANEMO = "Анемо"


class Area(str, Enum):
    INAZUMA = "Инадзума"
    LIYUE = "Ли Юэ"
    MONDSTADT = "Мондштадт"
    SNEZHNAYA = "Снежная"


class CharacterImage(BaseModel):
    link: str

    class Config:
        orm_mode = True


class Character(BaseModel):
    name: str
    rarity: Rarity
    element: Element
    weapon: Weapon
    sex: Sex
    area: Area
    images: list[CharacterImage]

    class Config:
        orm_mode = True


class Banner(BaseModel):
    name: str
    characters: list[Character]

    class Config:
        orm_mode = True
