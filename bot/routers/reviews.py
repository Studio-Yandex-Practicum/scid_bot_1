from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from api.api_points import handle_reviews_create  # функция для POST запроса


# Создаем FSM для управления состоянием
class ReviewStates(StatesGroup):
    waiting_for_review = State()


router = Router()

# Хендлер на команду 'review', которая запрашивает отзыв
@router.message(F.text == '/review')
async def start_review_process(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш отзыв.")
    # Состояние ожидания
    await state.set_state(ReviewStates.waiting_for_review)

# Хендлер для обработки текстового сообщения и отправки отзыва
@router.message(ReviewStates.waiting_for_review, F.text)
async def process_review(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # ID пользователя
    review_text = message.text  # Отзыв, который ввел пользователь

    # Отправляем POST запрос на API для сохранения отзыва
    response = await handle_reviews_create(user_id=user_id,
                                           review_text=review_text)

    if response:  # если API вернул успешный ответ
        await message.answer("Спасибо за ваш отзыв!")
    else:
        await message.answer("Произошла ошибка при отправке отзыва.")

    # Сбрасываем состояние пользователя
    await state.clear()
