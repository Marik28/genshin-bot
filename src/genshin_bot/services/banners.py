from typing import Optional

import sqlalchemy.orm

from .. import tables


class BannersService:
    def __init__(self, session: sqlalchemy.orm.Session):
        self.session = session

    def get_banner_by_name(self, banner_name: str) -> Optional[tables.Banner]:
        banner = (
            self.session.query(tables.Banner)
                .filter(tables.Banner.name == banner_name)
                .first()
        )
        return banner

    def get_list(self) -> list[tables.Banner]:
        banners = (
            self.session.query(tables.Banner)
                .all()
        )
        return banners
