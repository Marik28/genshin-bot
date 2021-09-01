from enum import Enum
from typing import Optional

from .users import BotUsersService
from .. import tables
from ..models.characters import Character, Rarity


class CharacterPicker:
    def pick(self, characters: list[tables.Character], rarity: Rarity) -> Optional[tables.Character]:
        """Возвращает случайного персонажа заданной редкости. Если редкость 3 звезды, возвращает None"""
        raise NotImplementedError


class StarRandomizer:
    drop_chances: Enum

    def roll_random_star(self) -> Rarity:
        """Возвращает случайную звезду от 3 до 5 на основе атрибута класса `drop_chances`"""
        raise NotImplementedError


class GuaranteeDropCounter:
    """Базовый класс счетчика молитв. Используется для ведения счета молитв, совершенных пользователем."""

    four_stars_drop_guarantee_rolls_amount: int = 10
    five_stars_drop_guarantee_rolls_amount: int = 90

    def __init__(self, user: tables.BotUser):
        self.user = user

    def calculate_guarantee(self, roll_star: Rarity, user: tables.BotUser) -> Rarity:
        """Рассчитывает гарантии 4 и 5 звезды"""
        if roll_star == Rarity.THREE:
            self.increment(Rarity.FOUR)
            self.increment(Rarity.FIVE)
        elif roll_star == Rarity.FOUR:
            self.reset(Rarity.FOUR)
            self.increment(Rarity.FIVE)
        elif roll_star == Rarity.FIVE:
            self.reset(Rarity.FIVE)
            self.reset(Rarity.FOUR)

        if self.get(Rarity.FIVE) == self.five_stars_drop_guarantee_rolls_amount:
            roll_star = Rarity.FIVE
            self.reset(Rarity.FIVE)
            self.reset(Rarity.FOUR)
        elif self.get(Rarity.FOUR) == self.four_stars_drop_guarantee_rolls_amount:
            roll_star = Rarity.FOUR
            self.reset(Rarity.FOUR)

        return roll_star

    def increment(self, star: Rarity) -> None:
        """Увеличивает счетчик совершенных молитв для данной редкости"""
        raise NotImplementedError

    def get(self, star: Rarity) -> int:
        """Возвращает количество молитв, с которых не выпал дроп данной редкости"""
        raise NotImplementedError

    def reset(self, star: Rarity) -> None:
        """Сбрасывает счетчик молитв для данной редкости"""
        raise NotImplementedError


class StarRoller:
    """Класс, реализующий логику выбивания редкости предмета с молитвы"""

    def roll_star(self, user: tables.BotUser, star_randomizer: StarRandomizer,
                  guarantee_drop_counter: GuaranteeDropCounter) -> Rarity:
        random_star = star_randomizer.roll_random_star()
        rolled_star = guarantee_drop_counter.calculate_guarantee(random_star, user)
        return rolled_star


class WishCounter:
    """Счетчик количества молитв по редкостям и в общем для пользователя"""

    def __init__(self, user: tables.BotUser, star: Rarity):
        self.user = user
        self.star = star

    def increment(self) -> None:
        """Увеличивает счетчик для выпавшей редкости и общий счетчик молитв"""
        self.increment_dropped_star()
        self.increment_total()

    def increment_dropped_star(self) -> None:
        """Увеличивает счетчик выпавших предметов с редкостью, которая передана в конструктор"""
        raise NotImplementedError

    def increment_total(self) -> None:
        """Увеличивает общий счетчик роллов"""
        raise NotImplementedError


class BaseCharacterWishService:
    def __init__(self,
                 user: tables.BotUser,
                 banner: tables.Banner,
                 character_picker: CharacterPicker,
                 star_roller: StarRoller,
                 star_randomizer: StarRandomizer,
                 guarantee_drop_counter: GuaranteeDropCounter,
                 bot_users_service: BotUsersService,
                 ):
        self.banner = banner
        self.user = user
        self.character_picker = character_picker
        self.star_roller = star_roller
        self.star_randomizer = star_randomizer
        self.guarantee_drop_counter = guarantee_drop_counter
        self.bot_users_service = bot_users_service

    def roll(self) -> Optional[Character]:
        star = self.star_roller.roll_star(self.user, self.star_randomizer, self.guarantee_drop_counter)
        result = self.character_picker.pick(self.banner.characters, star)
        if result is not None:
            self.bot_users_service.add_character_to_inventory(self.user, result)
        return result
