from enum import Enum
from random import random, choice
from typing import Optional

from .abc import StarRandomizer, GuaranteeDropCounter, CharacterPicker, StarRoller, WishCounter, \
    BaseCharacterWishService
from .redis import redis
from .. import tables
from ..models.characters import Rarity


class DefaultDropChances(Enum):
    five_stars = 0.006
    four_stars = 0.051
    three_stars = 0.943


class DefaultCharacterPicker(CharacterPicker):

    def pick(self, characters: list[tables.Character], rarity: Rarity) -> Optional[tables.Character]:
        if rarity == Rarity.THREE:
            return None
        this_rarity_characters = [character for character in characters if character.rarity == rarity]
        return choice(this_rarity_characters)


class DefaultStarRandomizer(StarRandomizer):
    drop_chances = DefaultDropChances

    def __init__(self):
        assert round((
                self.drop_chances.five_stars.value +
                self.drop_chances.four_stars.value +
                self.drop_chances.three_stars.value
        ), 4) == 1.0, "Суммарный шанс должен быть равен 1.0"

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

    def get_variable_name(self, star: Rarity):
        return f"{self.user.id}_{star}_star_rolls"

    def increment(self, star: Rarity):
        self.redis.incr(self.get_variable_name(star))

    def get(self, star: Rarity) -> int:
        return int(self.redis.get(self.get_variable_name(star)))

    def reset(self, star: Rarity) -> None:
        self.redis.set(self.get_variable_name(star), 0)


class DefaultStarRoller(StarRoller):
    pass


class GetRedisVariableNameMixin:
    def get_variable_name(self, user: tables.BotUser, star: Optional[Rarity]):
        star_bit = star.value if star is not None else "total"
        return f"{user.id}_{star_bit}_wishes_rolled"


# todo протестировать
class RedisWishCounter(WishCounter, GetRedisVariableNameMixin):
    redis = redis

    def increment_total(self) -> None:
        self.redis.incr(self.get_variable_name(self.user, None))

    def increment_dropped_star(self) -> None:
        self.redis.incr(self.get_variable_name(self.user, self.star))


class CharacterWishService(BaseCharacterWishService):
    pass
