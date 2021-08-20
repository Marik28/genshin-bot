from .bot import bot
from .settings import settings
from .database import engine
from .tables import Base

Base.metadata.create_all(engine)
bot.run(settings.discord_api_token)
