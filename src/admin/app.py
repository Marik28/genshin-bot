from flask import Flask

from genshin_bot.settings import settings

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.flask_secret_key
app.config['BASIC_AUTH_USERNAME'] = settings.basic_auth_username
app.config['BASIC_AUTH_PASSWORD'] = settings.basic_auth_password
