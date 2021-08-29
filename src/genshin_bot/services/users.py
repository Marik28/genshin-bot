from typing import Optional

import sqlalchemy.orm
from sqlalchemy.exc import IntegrityError

from .. import tables


class UsersService:
    def __init__(self, session: sqlalchemy.orm.Session):
        self.session = session

    def _get(self, user_id: int) -> Optional[tables.User]:
        user = (
            self.session.query(tables.User)
                .filter(tables.User.id == user_id)
                .first()
        )
        return user

    def create(self, user_id: int) -> tables.User:
        """
        Создает нового пользователя

        :raises tables.User.AlreadyExists: если пользователь с таким id уже существует
        """
        new_user = tables.User(id=user_id)
        self.session.add(new_user)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise tables.User.AlreadyExists from None
        return new_user

    def get_or_create(self, user_id: int) -> tables.User:
        user = self._get(user_id)
        if user is None:
            user = self.create(user_id)
        return user
