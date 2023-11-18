from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from app.admin.admin_keyboard import *
from app.user.user_keyboard import *
from data.database.db import *
from app.payment import *
import data.config as config

router = Router()


class AdminState(StatesGroup):
    set_message = State()
    set_prices = State()
    set_contacts = State()


@router.message(Command("admin"))
async def admin(message: Message):
    await message.answer("Вы вошли в админ панель", reply_markup=admin_keyboard())
    try:
        await message.delete()
    except:
        pass


@router.callback_query(F.data.startswith("back"))
async def back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вы вошли в админ панель", reply_markup=admin_keyboard())
    await state.clear()


@router.callback_query(F.data.startswith("statistic"))
async def statistic(call: CallbackQuery):
    dates = get_all_reg_date()
    for date in dates:
        dates[dates.index(date)] = datetime.datetime.fromisoformat(date[0])
    today = datetime.date.today()

    today_count = len([date for date in dates if date.date() == today])

    week_ago = today - datetime.timedelta(days=7)
    week_count = len([date for date in dates if week_ago <= date.date() <= today])
    all_time_count = len(dates)
    await call.message.edit_text(
        text=f"👥Статистика пользователей\n └ Сегодня: {today_count}\n └ За 7 дней: {week_count}\n └ Все время: {all_time_count}",
        reply_markup=cancel_and_back_keyboard())


@router.callback_query(F.data.startswith("set_mailing"))
async def send_mailing(call: CallbackQuery, state: FSMContext):
    await state.clear()
    m = await call.message.edit_text("Введите текст рассылки или отправьте картинку с описанием, для форматирования используйте HTML разметку", reply_markup=cancel_and_back_keyboard())
    await state.set_state(AdminState.set_message)
    await state.update_data(m_id=m.message_id)


@router.callback_query(F.data.startswith("replace_mailing"))
async def replace_mailing(call: CallbackQuery, state: FSMContext):
    await state.clear()
    m = await call.message.answer("Введите текст рассылки или отправьте картинку с описанием, для форматирования используйте HTML разметку", reply_markup=cancel_and_back_keyboard())
    await state.set_state(AdminState.set_message)
    await state.update_data(m_id=m.message_id)
    try:
        await call.message.delete()
    except:
        pass


@router.message(AdminState.set_message)
async def set_message(message: Message, state: FSMContext):
    if message.photo:
        if message.caption:
            text = message.caption
        else:
            text = ""
        try:
            await message.answer_photo(message.photo[-1].file_id, caption="Ваша рассылка:\n"+text, parse_mode="HTML", reply_markup=mailing_keyboard())
        except Exception as e:
            await message.answer(f"Ошибка: {e}\nПопробуйте еще раз", reply_markup=fail_mailing_keyboard())
        await state.update_data(message=text, photo=message.photo[-1].file_id)
    else:
        try:
            await message.answer("Ваша рассылка:\n" + message.text, parse_mode="HTML", reply_markup=mailing_keyboard())
        except Exception as e:
            await message.answer(f"Ошибка: {e}\nПопробуйте еще раз", reply_markup=fail_mailing_keyboard())

        await state.update_data(message=message.text, photo=None)
    try:
        await message.delete()
        data = await state.get_data()
        m_id = data.get("m_id")
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass


@router.callback_query(F.data.startswith("send_mailing"))
async def set_message(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("message")
    photo = data.get("photo")
    users = get_all_u_id()
    success = 0
    failed = 0
    print(message, photo, users)
    if photo:
        for user in users:
            try:
                await call.bot.send_photo(user[0], photo, caption=message, parse_mode="HTML", reply_markup=cancel_keyboard())
                success += 1
            except:
                failed += 1
    else:
        for user in users:
            try:
                await call.bot.send_message(user[0], message, parse_mode="HTML", reply_markup=cancel_keyboard())
                success += 1
            except:
                failed += 1
    await call.message.answer(f"Рассылка завершена\n└ Успешно: {success}\n└ Неудачно: {failed}", reply_markup=cancel_and_back_keyboard())
    await state.clear()
    try:
        await call.message.delete()
    except:
        pass


@router.callback_query(F.data.startswith("settings"))
async def settings(call: CallbackQuery):
    await call.message.edit_text("Настройки", reply_markup=settings_keyboard())


@router.callback_query(F.data.startswith("change_prices"))
async def change_prices(call: CallbackQuery, state: FSMContext):
    m = await call.message.edit_text(f"Введите новые цены через запятую\nВ порядке: 1месяц,3месяца,12месяцев,просмотр\nТекущие цены: <code>{config.subs_prices[0]},{config.subs_prices[1]},{config.subs_prices[2]},{config.view_price}</code>", parse_mode="HTML", reply_markup=cancel_and_back_keyboard())
    await state.set_state(AdminState.set_prices)
    await state.update_data(m_id=m.message_id)


@router.message(AdminState.set_prices)
async def set_prices(message: Message, state: FSMContext):
    prices = message.text.split(",")
    if len(prices) != 4:
        await message.answer("Неверное количество цен, попробуйте еще раз", reply_markup=cancel_keyboard())
        return
    try:
        for price in prices:
            float(price)
    except:
        await message.answer("Неверный формат цен, попробуйте еще раз", reply_markup=cancel_keyboard())
        return
    set_all_prices(prices[0], prices[1], prices[2], prices[3])
    config.update_config()
    await message.answer("Цены успешно изменены", reply_markup=cancel_and_back_keyboard())
    data = await state.get_data()
    m_id = data.get("m_id")
    try:
        await message.delete()
        await message.bot.delete_message(message.chat.id, m_id)
    except:
        pass


@router.callback_query(F.data.startswith("change_contacts"))
async def change_contacts(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Введите новые контакты\nТекущие контакты: <code>{config.admin_username}</code>", parse_mode="HTML", reply_markup=cancel_and_back_keyboard())
    await state.set_state(AdminState.set_contacts)


@router.message(AdminState.set_contacts)
async def set_contacts(message: Message, state: FSMContext):
    set_admin_username(message.text)
    config.update_config()
    await message.answer("Контакты успешно изменены", reply_markup=cancel_and_back_keyboard())
    try:
        await message.delete()
    except:
        pass

