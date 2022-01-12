from flask_admin import Admin

from genshin_bot.database import Session
from genshin_bot.settings import settings
from genshin_bot.tables import Character, Banner
from .app import app
from .views.banners import BannersView
from .views.characters import CharactersView

admin = Admin(app, name="genshin_bot", template_mode="bootstrap4", url=settings.admin_url)

with Session() as session:
    admin.add_view(CharactersView(Character, session))
    admin.add_view(BannersView(Banner, session))
    if __name__ == '__main__':
        app.run(
            host=settings.admin_app_host,
            port=settings.admin_app_port,
            debug=settings.debug,
        )
