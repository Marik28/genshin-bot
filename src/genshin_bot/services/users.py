from typing import Optional

import sqlalchemy.orm
from loguru import logger
from sqlalchemy.exc import IntegrityError

from .. import tables


class BotUsersService:
    def __init__(self, session: sqlalchemy.orm.Session):
        self.session = session

    def _get(self, user_id: int) -> Optional[tables.BotUser]:
        user = (
            self.session.query(tables.BotUser)
                .filter(tables.BotUser.id == user_id)
                .first()
        )
        return user

    def create(self, user_id: int, username: str) -> tables.BotUser:
        """
        Создает нового пользователя

        :raises tables.BotUser.AlreadyExists: если пользователь с таким id уже существует
        """
        new_user = tables.BotUser(id=user_id, username=username)
        self.session.add(new_user)
        try:
            self.session.commit()
        except IntegrityError as exc:
            logger.debug(str(exc))
            self.session.rollback()
            raise tables.BotUser.AlreadyExists from None
        return new_user

    def get_or_create(self, user_id: int, username: str) -> tuple[bool, tables.BotUser]:
        user = self._get(user_id)
        created = False
        if user is None:
            user = self.create(user_id, username)
            created = True
        return created, user

    def add_character_to_inventory(self, bot_user: tables.BotUser, character: tables.Character):
        logger.debug(bot_user.dropped_characters)
        bot_user.dropped_characters.append(character)
        self.session.add(bot_user)
        self.session.commit()

    def update_nickname(self, bot_user: tables.BotUser, new_username: str):
        bot_user.username = new_username
        self.session.add(bot_user)
        self.session.commit()
