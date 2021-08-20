import pytest

from genshin_bot.services.character_roller import DefaultStarRandomizer, DefaultStarRoller


@pytest.fixture(scope="session")
def user():
    class PseudoUser:
        def __init__(self):
            self.id = 1

    return PseudoUser()


@pytest.fixture(scope="session")
def default_star_randomizer():
    return DefaultStarRandomizer()


@pytest.fixture(scope="session")
def default_star_roller(user):
    return DefaultStarRoller(user)
