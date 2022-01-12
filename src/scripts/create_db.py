from genshin_bot.database import engine
from genshin_bot.tables import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
