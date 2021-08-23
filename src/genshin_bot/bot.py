from discord import User
from discord.ext import commands
from discord.ext.commands import Context
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from loguru import logger

from . import tables
from .models.banners import BannerList
from .services.character_roller import BaseCharacterWish
from .services.embed import CharacterEmbedService, BannerInfoEmbedService, WishesInfoEmbedService, \
    CommandsInfoEmbedService
from .services.wishes import WishesService
from .settings import settings

bot = commands.Bot(command_prefix=settings.command_prefix)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    logger.info("Бот подключился к серверу")


@bot.event
async def on_disconnect():
    logger.warning("Соединение с сервером потеряно")


@bot.event
async def on_command_error(ctx: Context, error):
    logger.error(f"In {ctx.guild}/{ctx.channel} (message by {ctx.message.author}): {error}.")


@slash.slash(
    name="help",
    description="Описание бота",
)
async def process_test_command(ctx: SlashContext):
    service = CommandsInfoEmbedService()
    embed = service.get_embed()
    await ctx.send(embed=embed)


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
        reply_message = f"{user.name} выбивает мусор 3 звезды из баннера {banner_name}"
        embed = None
    else:
        reply_message = None
        embed_service = CharacterEmbedService(user, result, banner_name)
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
async def process_banner_info_command(ctx: SlashContext, banner_name: str):
    service = BannerInfoEmbedService(banner_name)
    embed = service.get_embed()
    await ctx.channel.send(embed=embed)


@slash.slash(
    name="rolls_info",
    description="Статистика по роллам",
)
async def process_rolls_info_command(ctx: SlashContext):
    user = ctx.author
    service = WishesService()
    wishes_info = service.get_rolls_info(user)
    embed_service = WishesInfoEmbedService(user, wishes_info)
    embed = embed_service.get_embed()
    await ctx.channel.send(embed=embed)
