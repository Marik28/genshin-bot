from typing import Optional

from discord import User, Embed

from .base import EmbedService
from ..models.wishes import WishesInfo


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
