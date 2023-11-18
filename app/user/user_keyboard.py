from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types


def main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="💼Профиль"),
        types.KeyboardButton(text="❓О боте")
    )
    return builder.as_markup(resize_keyboard=True)


def main_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="❌Отмена")
    )
    return builder.as_markup(resize_keyboard=True)


def profile_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🔮Подписка", callback_data=f"subscription"),
            InlineKeyboardButton(text="🧿Просмотры", callback_data=f"views")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def guess_keyboard(username, name):
    buttons = [
        [
            InlineKeyboardButton(text="Узнать отправителя 🫣", callback_data=f"guess:{username}:{name}"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def quest_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"quest:yes"),
            InlineKeyboardButton(text="Нет", callback_data=f"quest:no")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def ask_buy_views_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🤫Купить просмотры", callback_data=f"buy_views:1")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def subscription_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="🔮1 месяц", callback_data=f"buy_subscription:1:месяц"),
            InlineKeyboardButton(text="🔮3 месяца", callback_data=f"buy_subscription:3:месяца"),
            InlineKeyboardButton(text="🔮12 месяцев", callback_data=f"buy_subscription:12:месяцев")
        ],
        [
            InlineKeyboardButton(text="◀️Назад", callback_data=f"back_profile")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def subscription_info_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="◀️Назад", callback_data=f"back_profile")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def buy_subscription_keyboard(link, p_id):
    buttons = [
        [
            InlineKeyboardButton(text="📎Оплатить", url=link)
        ],
        [
            InlineKeyboardButton(text="🔄Проверить оплату", callback_data=f"check_subscription_pay:{p_id}")
        ],
        [
            InlineKeyboardButton(text="❌Отмена", callback_data=f"back_profile")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def buy_views_keyboard(link, p_id):
    buttons = [
        [
            InlineKeyboardButton(text="📎Оплатить", url=link)
        ],
        [
            InlineKeyboardButton(text="🔄Проверить оплату", callback_data=f"check_views_pay:{p_id}")
        ],
        [
            InlineKeyboardButton(text="❌Отмена", callback_data=f"back_profile")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def views_keyboard():
    keyboard = InlineKeyboardBuilder()
    for i in range(1, 11):
        keyboard.add(InlineKeyboardButton(text=f"{i}", callback_data=f"buy_views:{i}"))
    keyboard.add(InlineKeyboardButton(text="◀️Назад", callback_data=f"back_profile"))
    return keyboard.adjust(5).as_markup()
