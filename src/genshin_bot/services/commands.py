from ..models.commands import Command, CommandArgument
from ..settings import settings

commands = [
    Command(
        name=f"{settings.command_prefix}roll",
        description="Сделать крутку",
        arguments=[
            CommandArgument(
                name="баннер",
                description="Баннер, который крутится. Список баннеров можно узнать слеш-командой /banners_info",
            )
        ],
    ),

    Command(
        name=f"/rolls_info",
        description="Узнать информацию и некоторую статистику о совершенных роллах"
    ),

    Command(
        name=f"/banner_info",
        description='Для того, чтобы узнать описание любой слеш-команды, просто нажми "/" и найди ее название'
    ),
]
