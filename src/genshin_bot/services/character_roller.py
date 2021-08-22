from enum import Enum
from random import random, choice
from typing import Optional, Type

from discord import User
from sqlalchemy import orm

from .abc import StarRandomizer, GuaranteeDropCounter, CharacterPicker, StarRoller, WishCounter
from .redis import redis
from .. import tables
from ..database import Session
from ..models.characters import Rarity, Character


class DefaultDropChances(Enum):
    five_stars = 0.006
    four_stars = 0.051
    three_stars = 0.943


class DefaultCharacterPicker(CharacterPicker):

    def __init__(self, banner_name: str):
        with Session() as session:  # type: orm.Session
            banner: tables.Banner = (
                session.query(tables.Banner)
                    .join(tables.Banner.characters)
                    .filter(tables.Banner.name == banner_name)
                    .first()
            )
            if banner is None:
                raise tables.Banner.DoesNotExist("Такого баннера нет")
            characters = banner.characters
            self.available_characters: list[Character] = [Character.from_orm(character) for character in characters]

    def pick(self, rarity: Rarity) -> Optional[Character]:
        if rarity == Rarity.THREE:
            return None
        this_rarity_characters = [character for character in self.available_characters if character.rarity == rarity]
        return choice(this_rarity_characters)


class DefaultStarRandomizer(StarRandomizer):
    drop_chances = DefaultDropChances

    def __init__(self):
        assert round(
            self.drop_chances.five_stars.value + self.drop_chances.four_stars.value + self.drop_chances.three_stars.value,
            4) == 1.0, "Суммарный шанс должен быть равен 1.0"

    def roll_random_star(self) -> Rarity:
        # todo подумать, как улучшить код
        random_number = random()

        if random_number <= self.drop_chances.five_stars.value:
            result = Rarity.FIVE
        elif (
                self.drop_chances.five_stars.value <
                random_number <=
                self.drop_chances.five_stars.value + self.drop_chances.four_stars.value
        ):
            result = Rarity.FOUR
        else:
            result = Rarity.THREE

        return result


class RedisGuaranteeDropCounter(GuaranteeDropCounter):
    redis = redis

    def get_star(self) -> Rarity:
        return self.roll_star

    def get_variable_name(self, star: Rarity):
        return f"{self.user.id}_{star}_star_rolls"

    def increment(self, star: Rarity):
        self.redis.incr(self.get_variable_name(star))

    def get(self, star: Rarity) -> int:
        return int(self.redis.get(self.get_variable_name(star)))

    def reset(self, star: Rarity) -> None:
        self.redis.set(self.get_variable_name(star), 0)


class DefaultStarRoller(StarRoller):
    star_randomizer: StarRandomizer = DefaultStarRandomizer()
    guarantee_drop_counter_cls = RedisGuaranteeDropCounter


class GetRedisVariableNameMixin:
    def get_variable_name(self, user: User, star: Optional[Rarity]):
        star_bit = star.value if star is not None else "total"
        return f"{user.id}_{star_bit}_wishes_rolled"


# todo протестировать
class RedisWishCounter(WishCounter, GetRedisVariableNameMixin):
    redis = redis

    def increment_total(self) -> None:
        self.redis.incr(self.get_variable_name(self.user, None))

    def increment_dropped_star(self) -> None:
        self.redis.incr(self.get_variable_name(self.user, self.star))


class BaseCharacterWish:
    character_picker_cls: Type[CharacterPicker] = DefaultCharacterPicker
    star_roller_cls: Type[StarRoller] = DefaultStarRoller
    wish_counter_cls: Type[WishCounter] = RedisWishCounter

    def __init__(self, user: User, banner_name: str):
        self.user = user
        self.character_picker = self.character_picker_cls(banner_name)
        self.star_roller = self.star_roller_cls(user)

    def roll(self) -> Optional[Character]:
        star = self.star_roller.roll_star()
        wish_counter = self.wish_counter_cls(self.user, star)
        wish_counter.increment()
        return self.character_picker.pick(star)


def get_banner(name: str) -> Optional[tables.Banner]:
    with Session() as session:  # type: orm.Session
        banner = session.query(tables.Banner).filter(tables.Banner.name == name).first()
    return banner
