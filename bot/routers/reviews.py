from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.backup.api_points import handle_reviews_create


# Создаем FSM для управления состоянием
class ReviewStates(StatesGroup):
    waiting_for_review = State()  # отзыв
    waiting_for_rating = State()  # оценка


router = Router()

# Хендлер на команду 'review', которая запрашивает отзыв
@router.message(F.text == '/review')
async def start_review_process(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш отзыв.")
    # Состояние ожидания
    await state.set_state(ReviewStates.waiting_for_review)


# Хендлер для получения текста отзыва и запроса оценки
@router.message(ReviewStates.waiting_for_review, F.text)
async def process_review(message: types.Message, state: FSMContext):
    review_text = message.text  # отзыв пользователя

    # Сохраняем отзыв в контексте состояния FSM
    await state.update_data(review_text=review_text)

    # Запрашиваем у пользователя оценку
    await message.answer("Пожалуйста, оцените от 1 до 5.")

    # Переводим пользователя в состояние ожидания оценки
    await state.set_state(ReviewStates.waiting_for_rating)

# Хендлер для обработки оценки и отправки данных в API
@router.message(ReviewStates.waiting_for_rating, F.text)
async def process_rating(message: types.Message, state: FSMContext):
    try:
        rating = int(message.text)
        if rating < 1 or rating > 5:
            raise ValueError  # Проверяем, что оценка от 1 до 5
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 5.")
        return

    # Получаем данные отзыва из состояния
    data = await state.get_data()
    review_text = data.get("review_text")
    user_id = message.from_user.id  # ID пользователя

    # Отправляем POST запрос на API для сохранения отзыва с оценкой
    response = await handle_reviews_create(user_id=user_id,
                                           review_text=review_text,
                                           rating=rating)

    if response:
        await message.answer("Спасибо за ваш отзыв и оценку!")
    else:
        await message.answer("Произошла ошибка при отправке отзыва.")

    # Сбрасываем состояние пользователя
    await state.clear()
