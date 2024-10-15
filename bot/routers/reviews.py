import json

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData

from api.api_reviews import handle_reviews_create


# Создаем FSM для управления состоянием
class ReviewStates(StatesGroup):
    waiting_for_review = State()  # отзыв
    waiting_for_rating = State()  # оценка


class ReviewRating(CallbackData, prefix="rating"):
    score: int


router = Router()

# Хендлер на команду 'review', которая запрашивает отзыв
@router.message(F.text == '/review')
async def start_review_process(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш отзыв.")
    # ждем ревью
    await state.set_state(ReviewStates.waiting_for_review)


# Хендлер для получения текста отзыва и показа кнопок для оценки
@router.message(ReviewStates.waiting_for_review, F.text)
async def process_review(message: types.Message, state: FSMContext):
    review_text = message.text  # отзыв

    # Сохраняем отзыв в контексте состояния FSM
    await state.update_data(review_text=review_text)

    # Создаем клавиатуру с оценками от 1 до 5
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(i),
                    callback_data=ReviewRating(score=i).pack()
                ) for i in range(1, 6)
            ]
        ]
    )

    # Отправляем сообщение с клавиатурой
    await message.answer("Пожалуйста, выберите оценку от 1 до 5:",
                         reply_markup=keyboard)

    # Переводим пользователя в состояние ожидания оценки
    await state.set_state(ReviewStates.waiting_for_rating)


# Хендлер для обработки выбора оценки через инлайн-кнопки
@router.callback_query(ReviewStates.waiting_for_rating,
                       ReviewRating.filter())
async def process_rating(callback_query: types.CallbackQuery,
                         callback_data: ReviewRating, state: FSMContext):
    # Получаем данные отзыва из состояния
    data = await state.get_data()
    review_text = data.get("review_text")
    user_id = callback_query.from_user.id  # ID пользователя

    # Отправляем POST запрос на API для сохранения отзыва с оценкой
    response = await handle_reviews_create(
        user_id=user_id,
        review_text=review_text,
        rating=callback_data.score
    )

    if 'detail' in response:  # если API вернул успешный ответ
        await callback_query.message.answer(json.dumps(response['detail']))
    else:
        await callback_query.message.answer("Спасибо за ваш отзыв и оценку!")

    # Убираем клавиатуру
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Сбрасываем состояние пользователя
    await state.clear()
    await callback_query.answer()
