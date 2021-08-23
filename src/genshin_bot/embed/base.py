from discord import Embed


class EmbedService:
    def get_embed(self) -> Embed:
        raise NotImplementedError
