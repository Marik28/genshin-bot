from genshin_bot.models.characters import Rarity


def test_random_distribution(default_star_randomizer):
    rolls_amount = 1_000_000
    rolls = [default_star_randomizer.roll_random_star() for _ in range(rolls_amount)]
    assert 0.005 < rolls.count(
        Rarity.FIVE) / rolls_amount < 0.007, "Шанс выпадения пятого дропа должен быть равен ~0.6%"
    assert 0.050 < rolls.count(Rarity.FOUR) / rolls_amount < 0.052, "Шанс выпадения четвертого дропа равен ~5.1%"


def test_five_drop_guarantee(default_star_roller, bot_user, default_star_randomizer, guarantee_drop_counter):
    for _ in range(100):
        rolls = [default_star_roller.roll_star(
            bot_user,
            default_star_randomizer,
            guarantee_drop_counter
        ) for __ in range(90)]
        assert len(rolls) == 90
        assert Rarity.FIVE in rolls, "За 90 роллов должен гарантированно упасть хотя бы 1 пятый дроп"


def test_four_drop_guarantee(default_star_roller, bot_user, default_star_randomizer, guarantee_drop_counter):
    for _ in range(100):
        rolls = [default_star_roller.roll_star(
            bot_user,
            default_star_randomizer,
            guarantee_drop_counter
        ) for __ in range(10)]
        assert len(rolls) == 10
        assert Rarity.FOUR in rolls or Rarity.FIVE in rolls, \
            "За 10 роллов должен упасть упасть гарантированно как минимум четвертый дроп"
