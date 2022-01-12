import requests
import typer

from genshin_bot.database import Session
from genshin_bot.settings import settings
from scripts.insert_data import insert_data
from scripts.parse_html import parse_characters

app = typer.Typer()


def download_page_content(url: str) -> bytes:
    response = requests.get(url)
    return response.content


@app.command(help="Скачивает инфу о персах, парсит её, и добавляет в БД")
def main(
        characters_url: str = typer.Option(
            settings.characters_url,
            help="URL статьи со списком персонажей на вики по геншину",
        ),
):
    typer.echo("Cкачивается страница с персонажами ...")
    page_content = download_page_content(characters_url)
    typer.echo("Скачана")
    characters = parse_characters(page_content)
    with Session() as session:
        insert_data(session, characters)


if __name__ == '__main__':
    app()
