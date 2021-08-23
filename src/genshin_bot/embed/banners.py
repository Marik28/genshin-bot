from typing import Optional

from discord import Embed

from .base import EmbedService
from .. import tables
from ..database import Session


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
