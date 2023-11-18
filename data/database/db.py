import sqlite3
import datetime
from os import system

path = "data/database/database.db"


def check_db():
    _ = system("cls")
    _datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    db = sqlite3.connect(path, check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        print("----   Database was found   ----")
    except sqlite3.OperationalError:
        print("----   Database not found   ----")
    print(f"-----   {_datetime}   -----")


def get_now_date():
    date = datetime.date.today()
    return date


def get_users_exist(user_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT u_id FROM users WHERE u_id = '{user_id}'")
    if cursor.fetchone() is None:
        return False
    else:
        return True


def add_user_to_db(user_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    if not (cursor.execute(f"SELECT u_id FROM users WHERE u_id = '{user_id}'").fetchone()):
        cursor.execute(
            f"INSERT INTO users(u_id, reg_date) VALUES ({user_id}, '{get_now_date()}')")
    db.commit()


def get_user_info(user_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE u_id = {user_id}")
    row = cursor.fetchone()
    return row


def add_count_mess(u_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET count_mess = count_mess + 1 WHERE u_id = {u_id}")
    db.commit()


def subtract_bought_views(u_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET bought_views = bought_views - 1 WHERE u_id = {u_id}")
    db.commit()


def check_subscription(user_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT subscription, sub_date FROM users WHERE u_id = {user_id}")
    row = cursor.fetchone()
    if row[0] == 0:
        return False
    elif row[1] is None:
        return False
    elif datetime.datetime.strptime(row[1], "%Y-%m-%d") < datetime.datetime.now():
        cursor.execute(f"UPDATE users SET subscription = 0 WHERE u_id = {user_id}")
        db.commit()
        return False
    else:
        return True


def add_subscription(user_id, month):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    date = datetime.date.today()
    cursor.execute(f"UPDATE users SET subscription = 1, sub_date = '{date + datetime.timedelta(days=int(month) * 30)}' WHERE u_id = {user_id}")
    db.commit()


def add_views(user_id, views):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET bought_views = bought_views + {views} WHERE u_id = {user_id}")
    db.commit()


def check_bought_views(user_id):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT bought_views FROM users WHERE u_id = {user_id}")
    row = cursor.fetchone()
    return row[0]


def get_subscriptions_price():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT sub_price_1m, sub_price_3m, sub_price_12m FROM settings")
    row = cursor.fetchone()
    return row


def get_subscription_price(month):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT sub_price_{month}m FROM settings")
    row = cursor.fetchone()
    return row[0]


def get_views_price():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT views_price FROM settings")
    row = cursor.fetchone()
    return row[0]


def get_admin_username():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT admin_username FROM settings")
    row = cursor.fetchone()
    return row[0]


def set_admin_username(username):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET admin_username = '{username}'")
    db.commit()


def get_all_reg_date():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT reg_date FROM users")
    row = cursor.fetchall()
    return row


def get_all_u_id():
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT u_id FROM users")
    row = cursor.fetchall()
    return row


def set_all_prices(sub_price_1m, sub_price_3m, sub_price_12m, views_price):
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET sub_price_1m = {sub_price_1m}, sub_price_3m = {sub_price_3m}, sub_price_12m = {sub_price_12m}, views_price = {views_price}")
    db.commit()


