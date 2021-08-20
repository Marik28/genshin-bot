from discord import User
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from loguru import logger

from . import tables
from .models.banners import BannerList
from .services.character_roller import BaseCharacterWish
from .services.embed import CharacterEmbedService, BannerInfoEmbedService
from .settings import settings

bot = commands.Bot(command_prefix=settings.command_prefix)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    logger.info("Бот подключился к серверу")


@bot.event
async def on_disconnect():
    logger.warning("Соединение с сервером потеряно")


@bot.command(name="roll")
async def process_roll_command(ctx: Context, banner_name: str = BannerList.DEFAULT.value):
    user: User = ctx.message.author
    try:
        roller = BaseCharacterWish(user, banner_name)
    except tables.Banner.DoesNotExist as exc:
        await ctx.send(str(exc))
        return

    result = roller.roll()

    if result is None:
        reply_message = f"{user.name} выбивает мусор 3 звезды"
        embed = None
    else:
        reply_message = None
        embed_service = CharacterEmbedService(user, result)
        embed = embed_service.get_embed()

    await ctx.send(content=reply_message, embed=embed)


@slash.slash(
    name="banner_info",
    description="Информация о баннере",
    options=[
        create_option(
            name="banner_name",
            description="Название баннера",
            option_type=3,
            required=True,
            choices=[banner for banner in BannerList]
        ),
    ]
)
async def process_banner_info_command(ctx: Context, banner_name: str):
    service = BannerInfoEmbedService(banner_name)
    embed = service.get_embed()
    await ctx.send(embed=embed)
