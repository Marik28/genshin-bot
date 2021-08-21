from enum import Enum
from typing import Optional, Type

from discord import User

from ..models.characters import Character, Rarity


class CharacterPicker:
    def pick(self, rarity: Rarity) -> Optional[Character]:
        """Возвращает случайного персонажа"""
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

    def __init__(self, user: User, roll_star: Rarity):
        self.user = user
        self.roll_star = roll_star

    def calculate_guarantee(self):
        """Рассчитывает гарантии 4 и 5 звезды"""
        if self.roll_star == Rarity.THREE:
            self.increment(Rarity.FOUR)
            self.increment(Rarity.FIVE)
        elif self.roll_star == Rarity.FOUR:
            self.reset(Rarity.FOUR)
            self.increment(Rarity.FIVE)
        elif self.roll_star == Rarity.FIVE:
            self.reset(Rarity.FIVE)
            self.reset(Rarity.FOUR)

        if self.get(Rarity.FIVE) == self.five_stars_drop_guarantee_rolls_amount:
            self.roll_star = Rarity.FIVE
            self.reset(Rarity.FIVE)
            self.reset(Rarity.FOUR)
        elif self.get(Rarity.FOUR) == self.four_stars_drop_guarantee_rolls_amount:
            self.roll_star = Rarity.FOUR
            self.reset(Rarity.FOUR)

    def increment(self, star: Rarity) -> None:
        """Увеличивает счетчик совершенных молитв для данной редкости"""
        raise NotImplementedError

    def get(self, star: Rarity) -> int:
        """Возвращает количество молитв, с которых не выпал дроп данной редкости"""
        raise NotImplementedError

    def reset(self, star: Rarity) -> None:
        """Сбрасывает счетчик молитв для данной редкости"""
        raise NotImplementedError

    def get_star(self) -> Rarity:
        """Возвращает редкость, которая выпала с учетом корректировки счетчика молитв"""
        raise NotImplementedError


class StarRoller:
    """Класс, реализующий логику выбивания редкости предмета с молитвы"""

    star_randomizer: StarRandomizer
    guarantee_drop_counter_cls: Type[GuaranteeDropCounter]

    def __init__(self, user: User):
        self.user = user

    def roll_star(self) -> Rarity:
        random_star = self.star_randomizer.roll_random_star()
        guarantee_drop_counter = self.guarantee_drop_counter_cls(self.user, random_star)
        guarantee_drop_counter.calculate_guarantee()
        rolled_star = guarantee_drop_counter.get_star()
        return rolled_star
