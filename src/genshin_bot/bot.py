from discord import User
from discord.ext import commands
from discord.ext.commands import Context, CommandInvokeError
from discord.member import Member
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from loguru import logger

from .database import Session
from .embed.banners import BannerInfoEmbedService
from .embed.characters import CharacterEmbedService
from .embed.commands import CommandsInfoEmbedService
from .embed.wishes import WishesInfoEmbedService
from .models.banners import BannerList
from .services.banners import BannersService
from .services.character_roller import CharacterWishService, DefaultCharacterPicker, DefaultStarRoller, \
    DefaultStarRandomizer, RedisGuaranteeDropCounter
from .services.users import BotUsersService
from .services.wishes import WishesService
from .settings import settings

bot = commands.Bot(
    command_prefix=settings.command_prefix,
)
slash = SlashCommand(bot, sync_commands=True)
logger.add(settings.base_dir / "logs.log", level="INFO", rotation="2 MB")


@bot.event
async def on_ready():
    logger.info("Бот подключился к серверу")


@bot.event
async def on_disconnect():
    logger.warning("Соединение с сервером потеряно")


@bot.event
async def on_command_error(ctx: Context, error: CommandInvokeError):
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
    with Session() as session:
        discord_user: Member = ctx.message.author
        bot_users_service = BotUsersService(session)
        _, bot_user = bot_users_service.get_or_create(discord_user.id, discord_user.name)
        banners_service = BannersService(session)
        banner = banners_service.get_banner_by_name(banner_name)
        if banner is None:
            await ctx.send("Такого баннера нет")
            return

        roller = CharacterWishService(
            user=bot_user,
            banner=banner,
            character_picker=DefaultCharacterPicker(),
            star_roller=DefaultStarRoller(),
            star_randomizer=DefaultStarRandomizer(),
            guarantee_drop_counter=RedisGuaranteeDropCounter(bot_user),
            bot_users_service=bot_users_service
        )
        result = roller.roll()

        if result is None:
            reply_message = f"{discord_user.name} выбивает мусор 3 звезды из баннера {banner_name}"
            embed = None
        else:
            reply_message = None
            embed_service = CharacterEmbedService(discord_user, result, banner_name)
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


@bot.event
async def on_user_update(before: User, after: User):
    logger.debug(f"{before.name, before.id, after.name, after.id}")
    with Session() as session:
        bot_users_service = BotUsersService(session)
        created, bot_user = bot_users_service.get_or_create(after.id, after.name)
        if not created:
            bot_users_service.update_nickname(after.id, after.name)
