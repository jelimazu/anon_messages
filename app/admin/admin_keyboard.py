from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from data.database.db import *
import data.config as config


def admin_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📊Статистика", callback_data=f"statistic"),
        ],
        [
            InlineKeyboardButton(text="📨Рассылка", callback_data=f"set_mailing"),
        ],
        [
            InlineKeyboardButton(text="⚙️Настройки", callback_data=f"settings"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_and_back_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"back"),
            InlineKeyboardButton(text="❌", callback_data=f"cancel")

        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mailing_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📢Отправить", callback_data=f"send_mailing"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"back"),
            InlineKeyboardButton(text="🔄", callback_data=f"replace_mailing"),
            InlineKeyboardButton(text="❌", callback_data=f"cancel")

        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fail_mailing_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"back"),
            InlineKeyboardButton(text="🔄", callback_data=f"replace_mailing"),
            InlineKeyboardButton(text="❌", callback_data=f"cancel")

        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def settings_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📈Изменить цены", callback_data=f"change_prices"),
        ],
        [
            InlineKeyboardButton(text="📇Изменить контакты", callback_data=f"change_contacts"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"back"),
            InlineKeyboardButton(text="❌", callback_data=f"cancel")

        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard