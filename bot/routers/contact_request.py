import re

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from api.api_managers import create_contact_request
from core.config import settings
from keyboards.contact_request import (
    ContactViaCallback,
    CONTACT_REQUEST_CANCEL_MENU,
    CONTACT_REQUEST_CONTACT_VIA_MENU,
    CONTACT_REQUEST_GET_EMAIL_BUTTON,
    CONTACT_REQUEST_GET_PHONE_BUTTON,
    CONTACT_REQUEST_SEND_REQUEST_MENU,
    CONTACT_REQUEST_START_BUTTON
)
from utils.manager_state import ContactRequestState


router = Router()


@router.message(Command("request_contact"))
async def contact_request_start(message: types.Message, state: FSMContext):
    """Обработка команды /request_contact"""
    await state.set_state(ContactRequestState.start)
    await state.update_data(
        current_user_username=message.from_user.username,
        current_user_id=message.from_user.id
    )
    await message.answer(
        text=(
            "Задайте вопрос менеджеру, указав удобный способ для связи "
            "и наш менеджер поможет Вам!"
        ),
        reply_markup=CONTACT_REQUEST_START_BUTTON
    )


@router.message(
    F.text == "🔚 Отменить запрос на обратную связь"
)
async def contact_request_cancel_request(
    message: types.Message,
    state: FSMContext
):
    """Отмена запроса на обратную связь"""
    await state.clear()
    await message.answer(
        text=("Ваш запрос отменён")
    )


@router.callback_query(ContactRequestState.start)
async def contact_request_wait_question(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Запрос вопроса пользователя"""
    await state.set_state(ContactRequestState.enter_question)
    await callback.message.answer(
        text=("Введите Ваш вопрос"),
        reply_markup=CONTACT_REQUEST_CANCEL_MENU
    )


@router.message(
    ContactRequestState.enter_question,
    F.text != "🔚 Отменить запрос на обратную связь"
)
async def contact_request_wait_phone(
    message: types.Message,
    state: FSMContext
):
    """Запрос телефона пользователя"""
    await state.update_data(question=message.text)
    await state.set_state(ContactRequestState.enter_phone)
    await message.reply(
        text=("Вопрос принят.\nОтправьте Ваш номер телефона"),
        reply_markup=CONTACT_REQUEST_GET_PHONE_BUTTON
    )


@router.message(ContactRequestState.enter_phone)
@router.message(F.contact)
async def contact_request_wait_email(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):
    """Запрос email пользователя"""
    text = "Отправьте Ваш e-mail"
    await state.update_data(phone=None)
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        text = "Ваш номер сохранён.\n\nОтправьте Ваш e-mail"
    await state.set_state(ContactRequestState.enter_email)
    await message.answer(
        text=text,
        reply_markup=CONTACT_REQUEST_GET_EMAIL_BUTTON
    )

@router.message(ContactRequestState.enter_email)
async def contact_request_wait_contact_via(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):
    """Запрос удобного способа связи для пользователя"""
    text = "Выберите, удобный для Вас, способ связи"
    await state.update_data(email=None)
    if message.text != "🚫 Не отправлять e-mail":
        email = message.text
        if re.fullmatch(settings.validation.regex_email_validation, email):
            await state.update_data(email=email)
            await state.set_state(ContactRequestState.end)
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            text = (
                "Ваш e-mail сохранён.\n\nВыберите, удобный для Вас, "
                "способ связи"
            )
        else:
            await message.answer(text="E-mail некорректен")
            return await contact_request_wait_email(
                message=message,
                state=state,
                bot=bot
            )
    await state.set_state(ContactRequestState.enter_contact_via)
    await message.answer(
        text=text,
        reply_markup=CONTACT_REQUEST_CONTACT_VIA_MENU
    )


@router.callback_query(
    ContactRequestState.enter_contact_via,
    ContactViaCallback.filter()
)
async def contact_request_check_response(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: ContactViaCallback
):
    """Проверка запроса пользователя"""
    data = await state.get_data()
    tg = data["current_user_username"] if data["current_user_username"] else ""
    phone = data["phone"] if data["phone"] else ""
    email = data["email"] if data["email"] else ""
    text = (
        f"<b>Ваш вопрос:</b>\n {data['question']}\n\n"
        f"Контакты:\n"
        f"<b>Телеграм:</b> @{tg}\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>E-mail:</b> {email}\n"
        f"<b>Способ связи:</b> {callback_data.contact_type}"
    )
    await state.update_data(
        contact_via_type=callback_data.contact_type,
        info_message_id=callback.message.message_id
    )
    await state.set_state(ContactRequestState.end)
    await callback.message.answer(
        text=text,
        reply_markup=CONTACT_REQUEST_SEND_REQUEST_MENU
    )


@router.message(
    ContactRequestState.end
)
async def contact_request_send_response(
    message: types.Message,
    state: FSMContext,
    bot: Bot
):
    """Отправка запроса"""
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=data["info_message_id"]
    )
    
    response = await create_contact_request(data)
    if 'detail' not in response:
        await state.clear()
        return await message.answer(
            text=(
                "Ваша заявка отправлена. Наш менеджер свяжится с Вами "
                "в ближайщее время"
            )
        )
    await message.answer(
        text=f"Во время создания заявки произошла ошибка: {response['detail']}"
    )