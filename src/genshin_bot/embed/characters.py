import random

from discord import Embed, Member

from .base import EmbedService
from .. import tables
from ..models import Element, Rarity


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

    def __init__(self, user: Member, character: tables.Character, banner_name: str):
        self.user = user
        self.banner = banner_name
        self.character = character
        self.embed = Embed()
        self.add_character_info()

    def add_character_info(self):
        self.embed.title = f"Результат ролла баннера {self.banner} пользователем {self.user.name}"
        self.embed.add_field(name="Редкость", value=self.generate_rating(), inline=False)
        self.embed.add_field(name="Имя", value=f"{self.character.name} {self.get_element_emoji()}")
        image = str(random.choice(self.character.images).link) if self.character.images else self.default_image
        self.embed.set_image(url=image)
        self.embed.colour = self.get_rarity_color()

    def get_embed(self) -> Embed:
        return self.embed

    def generate_rating(self) -> str:
        """Отрисовывает звездочки по 5-звездочной шкале"""
        rating = "★" * self.character.rarity
        return f"{rating:☆<5}"

    def get_rarity_color(self) -> int:
        return self.rarity_colors[self.character.rarity]

    def get_element_emoji(self) -> str:
        return self.elements[self.character.element]
