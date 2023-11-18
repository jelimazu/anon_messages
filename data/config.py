import configparser
from aiogram.types import User

import data.database.db as db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs.txt')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8')
data = config["settings"]
token = data["token"]
admin_id = list(map(int, data["admin_id"].split(",")))
bot_username = str
bot_name = str
admin_username = db.get_admin_username()
subs_prices = db.get_subscriptions_price()
view_price = db.get_views_price()


def update_config():
    global admin_username
    global subs_prices
    global view_price

    admin_username = db.get_admin_username()
    subs_prices = db.get_subscriptions_price()
    view_price = db.get_views_price()


def update_bot_info(user: User):
    global bot_username
    global bot_name

    bot_username = user.username
    bot_name = user.first_name


