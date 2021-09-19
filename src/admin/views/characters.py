from genshin_bot.models import Rarity, Element, Weapon, Sex, Area
from genshin_bot.tables import CharacterImage
from .base import BaseModelView
from ..services.choices import make_choices


class CharactersView(BaseModelView):
    inline_models = [CharacterImage]
    column_details_list = ["name", "rarity", "element", "weapon", "sex", "Area", "banners"]
    form_choices = {
        "rarity": make_choices(Rarity),
        "element": make_choices(Element),
        "weapon": make_choices(Weapon),
        "sex": make_choices(Sex),
        "area": make_choices(Area),
    }
