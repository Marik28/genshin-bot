from enum import EnumMeta


def make_choices(enum: EnumMeta) -> list[tuple[str, str]]:
    """Формирует список формата

    [
        ('CHOICE_NAME', 'choice_value'),

        ('CHOICE_NAME', 'choice_value'),

    ]

    из переданного перечисления

    :param enum: название класса перечисления, из которого необходимо составить список
    """
    return [(key, value) for key, value in {choice.value: choice.name for choice in enum}.items()]
