import random
from typing import Optional

from discord import Embed, User

from .. import tables
from ..database import Session
from ..models.characters import Character, Element, Rarity
from ..models.wishes import WishesInfo


class EmbedService:
    def get_embed(self) -> Embed:
        raise NotImplementedError


class CharacterEmbedService(EmbedService):
    elements = {
        Element.ELECTRO: "⚡",
        Element.PYRO: "🔥",
        Element.ANEMO: "💨",
        Element.CRYO: "❄",
        Element.HYDRO: "🌊",
        Element.GEO: "🌎",
    }
    rarity_colors = {
        Rarity.FIVE: 0xFFD700,
        Rarity.FOUR: 0x800080,
        Rarity.THREE: 0x0F52BA,
    }

    default_image = "https://static.wikia.nocookie.net/gensin-impact/images/1/1b/Character_Paimon_Portrait.png/revision/latest?cb=20201205191049"

    def __init__(self, user: User, character: Character, banner_name: str):
        self.user = user
        self.banner = banner_name
        self.character = character
        self.embed = Embed()
        self.add_character_info()

    def add_character_info(self):
        self.embed.title = f"Результат ролла баннера {self.banner} пользователем {self.user.name}"
        self.embed.add_field(name="Редкость", value=self.generate_rating(), inline=False)
        self.embed.add_field(name="Имя", value=f"{self.character.name} {self.get_element_emoji()}")
        image = random.choice(self.character.images).link if self.character.images else self.default_image
        self.embed.set_image(url=image)
        self.embed.colour = self.get_rarity_color()

    def get_embed(self) -> Embed:
        return self.embed

    def generate_rating(self) -> str:
        """Отрисовывает звездочки по 5-звездночной шкале"""
        rating = "★" * self.character.rarity.value
        return f"{rating:☆<5}"

    def get_rarity_color(self) -> int:
        return self.rarity_colors[self.character.rarity]

    def get_element_emoji(self) -> str:
        return self.elements[self.character.element]


class BannerInfoEmbedService(EmbedService):
    def __init__(self, banner_name: str):
        with Session() as session:
            banner: Optional[tables.Banner] = (
                session.query(tables.Banner)
                    .filter(tables.Banner.name == banner_name)
                    .join(tables.Banner.characters)
                    .first()
            )
            if banner is None:
                raise tables.Banner.DoesNotExist
            self.banner = banner
            self.embed = Embed()
            self.add_banner_info()

    def get_embed(self) -> Embed:
        return self.embed

    def add_banner_info(self):
        self.embed.title = f"Информация о баннере {self.banner.name}"
        self.embed.add_field(name="Персонажи", value=', '.join([char.name for char in self.banner.characters]))


class WishesInfoEmbedService(EmbedService):
    def __init__(self, user: User, wishes_info: WishesInfo):
        self.user = user
        self.wishes_info = wishes_info
        self.embed = Embed()
        self.add_wishes_info()

    def add_wishes_info(self):
        self.embed.title = f"Информация о роллах {self.user.name}"
        self.embed.add_field(
            name="Всего роллов",
            value=str(self.wishes_info.total_rolls_done),
            inline=False,
        )
        self.embed.add_field(
            name="5 звездочных персонажей",
            value=str(self.wishes_info.five_drops_amount),
            inline=False,
        )
        self.embed.add_field(
            name="Процент 5 звездочных",
            value=f"{(self.calculate_percentage(self.wishes_info.five_drops_amount, self.wishes_info.total_rolls_done))}"
        )
        self.embed.add_field(
            name="4 звездочных персонажей",
            value=str(self.wishes_info.four_drops_amount),
            inline=False,
        )
        self.embed.add_field(
            name="Процент 4 звездочных",
            value=f"{(self.calculate_percentage(self.wishes_info.four_drops_amount, self.wishes_info.total_rolls_done))}"
        )

    def calculate_percentage(self, value: Optional[int], total: Optional[int]) -> str:
        if total is None or value is None:
            percentage = 0.0
        else:
            percentage = value / total
        return f"{percentage:.2%}"

    def get_embed(self) -> Embed:
        return self.embed
