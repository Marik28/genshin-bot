from loguru import logger

from genshin_bot import tables


def test_add_character_method(session, bot_user, bot_users_service):
    character = session.query(tables.Character).first()
    logger.debug(character.name)
    logger.debug([char.name for char in bot_user.characters_in_possession])
    chars_before = len(bot_user.characters_in_possession)
    bot_users_service.add_character_to_inventory(bot_user, character)
    chars_after = len(bot_user.characters_in_possession)
    assert chars_after - chars_before == 1
