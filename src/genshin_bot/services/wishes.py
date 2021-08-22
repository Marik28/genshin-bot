from discord import User

from .character_roller import GetRedisVariableNameMixin
from .redis import redis
from ..models import Rarity
from ..models.wishes import WishesInfo


class WishesService(GetRedisVariableNameMixin):
    redis = redis

    def get(self, name: str):
        """Возвращает значение по ключу из Redis"""
        return self.redis.get(name)

    def get_rolls_info(self, user: User) -> WishesInfo:
        wishes_info_dict = {
            "five_drops_amount": self.get(self.get_variable_name(user, Rarity.FIVE)),
            "four_drops_amount": self.get(self.get_variable_name(user, Rarity.FOUR)),
            "total_rolls_done": self.get(self.get_variable_name(user, None))
        }
        return WishesInfo.parse_obj(wishes_info_dict)
