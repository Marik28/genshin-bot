import pytest

from genshin_bot.database import Session
from genshin_bot.services.character_roller import DefaultStarRandomizer, DefaultStarRoller, RedisGuaranteeDropCounter
from genshin_bot.services.users import BotUsersService


@pytest.fixture(scope="session")
def bot_users_service(session):
    return BotUsersService(session)


@pytest.fixture(scope="session")
def bot_user(bot_users_service):
    _, user = bot_users_service.get_or_create(1, "test_user")
    return user


@pytest.fixture(scope="session")
def default_star_randomizer():
    return DefaultStarRandomizer()


@pytest.fixture(scope="session")
def default_star_roller():
    return DefaultStarRoller()


@pytest.fixture(scope="session")
def session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def guarantee_drop_counter(bot_user):
    return RedisGuaranteeDropCounter(bot_user)
