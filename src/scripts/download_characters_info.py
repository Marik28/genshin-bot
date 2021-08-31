from time import time

import requests
from loguru import logger

from genshin_bot.settings import settings

html_dir = settings.base_dir / "data" / "html"
if not html_dir.exists():
    html_dir.mkdir()

characters_url = "https://genshin-impact.fandom.com/ru/wiki/%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8"
logger.debug(f"Ссылка на страницу с данными о персонажах - {characters_url}")


def download_page_and_save_html(url: str) -> None:
    response = requests.get(url)
    html = response.content
    filename = f"genshin-{int(time())}.html"
    with open(html_dir / filename, "wb") as file:
        file.write(html)
    logger.info(f"Файл сохранен в  {html_dir / filename}")


if __name__ == '__main__':
    download_page_and_save_html(characters_url)
