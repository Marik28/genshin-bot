from time import time

import requests

from genshin_bot.settings import settings

html_dir = settings.base_dir / "data" / "html"
print(html_dir)

characters_url = "https://genshin-impact.fandom.com/ru/wiki/%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8"


def download_page_and_save_html(url: str) -> None:
    response = requests.get(url)
    html = response.content
    filename = f"genshin-{int(time())}.html"
    with open(html_dir.absolute() / filename, "wb") as file:
        file.write(html)
    print(f"Скачан файл {filename}")


if __name__ == '__main__':
    download_page_and_save_html(characters_url)
