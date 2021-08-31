import argparse
import json

import requests
from bs4 import BeautifulSoup

from ..settings import settings

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Файл с html, который необходимо распарсить в json")

html_dir = settings.base_dir / "data" / "html"
json_dir = settings.base_dir / "data" / "json"

GENSHIN_WIKI_BASE_URL = 'https://genshin-impact.fandom.com'


def replace_spaces(character_name: str) -> str:
    character_name = character_name.replace("\n", " ").strip()
    while "  " in character_name:
        character_name = character_name.replace("  ", " ")
    return character_name


def write_json(obj, file_name: str):
    with open(json_dir / file_name, "w") as file:
        json.dump(obj, file, ensure_ascii=False, indent=2)


def get_character_image_link(character_url: str) -> str:
    r = requests.get(f"{GENSHIN_WIKI_BASE_URL}{character_url}")
    soup = BeautifulSoup(r.content, "lxml")
    image = soup.select_one("figure.pi-item.pi-image img")
    return image.attrs["src"]


def parse_html_to_json(html_filename: str):
    with open(html_dir / html_filename, "r") as file:
        content = file.read()
    soup = BeautifulSoup(content, "lxml")
    tables = soup.select("table.article-table.sortable")
    characters_list_table: BeautifulSoup = tables[0]
    characters_list = []
    for row in characters_list_table.find_all("tr")[1:]:
        columns = row.find_all("td")
        stars = int(columns[2].select_one("p img").attrs["alt"].split(" ")[0])
        name = replace_spaces(columns[1].text)
        character_link = columns[1].find("a").attrs["href"]
        image_link = get_character_image_link(character_link)
        if name == "Путешественник":
            continue
        gods_eye = columns[3].text.strip()
        weapon = columns[4].text.strip()
        sex = columns[5].text.strip()
        area = columns[6].find("a").text.strip()
        character = {
            "rarity": stars,
            "name": name,
            "element": gods_eye,
            "weapon": weapon,
            "sex": sex,
            "area": area,
            "images": [
                {
                    "link": image_link,
                }
            ]
        }
        characters_list.append(character)
        print(stars, name, gods_eye, weapon, sex, area)
    json_file_name = html_filename.replace(".html", ".json")
    write_json(characters_list, json_file_name)
    print(f"Сохранено в файле {json_file_name}")


if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    parse_html_to_json(filename)
