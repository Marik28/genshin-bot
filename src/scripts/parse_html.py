import random
import time
from typing import (
    Union,
    Optional,
)
from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
)

import requests
import typer
from bs4 import BeautifulSoup
from bs4.element import PageElement

from genshin_bot.models.characters import (
    Character,
    CharacterImage,
    Rarity,
)
from genshin_bot.settings import settings


def replace_spaces(character_name: str) -> str:
    character_name = character_name.replace("\n", " ").strip()
    while "  " in character_name:
        character_name = character_name.replace("  ", " ")
    return character_name


def get_character_image_link(character_url: str) -> str:
    r = requests.get(f"{settings.genshin_wiki_base_url}{character_url}")
    soup = BeautifulSoup(r.content, "lxml")
    image = soup.select_one("figure.pi-item.pi-image img")
    image_url = urlparse(image.attrs["src"])
    query = parse_qs(image_url.query)
    query.pop("cb", None)
    image_url = image_url._replace(query=urlencode(query, doseq=True)).geturl()
    print("url", image_url)
    return image_url


def parse_row(row: PageElement) -> Optional[Character]:
    """
    :return: Parsed Character or None if character is a traveler or does not have area
    """
    columns = row.find_all("td")
    stars = Rarity(
        int(
            columns[2]
                .select_one("p img")
                .attrs["alt"]
                .split(" ")[0]
        )
    )
    name = replace_spaces(columns[1].text)
    character_link = columns[1].find("a").attrs["href"]
    image_link = get_character_image_link(character_link)
    if name == "Путешественник":
        return None
    gods_eye = columns[3].text.strip()
    weapon = columns[4].text.strip()
    sex = columns[5].text.strip()
    try:
        area = columns[6].find("a").text.strip()
    except AttributeError:
        return None
    return Character(
        rarity=stars,
        name=name,
        element=gods_eye,
        weapon=weapon,
        sex=sex,
        area=area,
        images=[CharacterImage(link=image_link)]
    )


def parse_characters(page_content: Union[bytes, str]) -> list[Character]:
    soup = BeautifulSoup(page_content, "lxml")
    tables = soup.select("table.article-table.sortable")
    characters_list_table = tables[0]
    parsed_characters = []
    rows = characters_list_table.find_all("tr")[1:]
    with typer.progressbar(rows, label="Парсинг персонажей", length=len(rows)) as progress:
        for row in progress:
            character = parse_row(row)
            if character is not None:
                parsed_characters.append(character)
            sleep_secs = random.randrange(2, 5) / 10
            time.sleep(sleep_secs)
    return parsed_characters


__all__ = ['parse_characters']
