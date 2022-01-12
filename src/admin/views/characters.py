from flask_admin.model.template import macro

from genshin_bot.models import Rarity, Element, Weapon, Sex, Area
from genshin_bot.tables import CharacterImage, Banner
from .base import BaseModelView
from ..services.choices import make_choices


class CharactersView(BaseModelView):
    inline_models = [CharacterImage, Banner]
    column_details_list = ["name", "rarity", "element", "weapon", "sex", "area", "banners", "images"]
    column_searchable_list = ["name"]
    column_list = ["name", "rarity", "weapon", "element"]
    column_default_sort = "name"
    form_choices = {
        "rarity": make_choices(Rarity),
        "element": make_choices(Element),
        "weapon": make_choices(Weapon),
        "sex": make_choices(Sex),
        "area": make_choices(Area),
    }
    details_template = "characters/details.html"
    list_template = "characters/list.html"
    column_formatters_detail = {
        "images": macro("render_character_image"),
        "banners": macro("render_character_banner"),
    }
    column_formatters = {
        "name": macro("render_character_name")
    }
