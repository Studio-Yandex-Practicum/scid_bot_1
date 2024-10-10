from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

API_URL = 'https://example.com/api'


# Функция для генерации клавиатуры - Кнопки через API
async def fetch_buttons_from_api(endpoint_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            # Выполняем GET-запрос к API, чтобы получить кнопки для конкретного endpoint_id
            async with session.get(f"{API_URL}/buttons/{endpoint_id}") as response:
                if response.status == 200:
                    # Парсим ответ в JSON формате
                    data = await response.json()
                    # Возвращаем список кнопок из ответа API
                    return data.get('buttons', [])
                else:
                    # В случае ошибки возвращаем пустой список
                    return []
        except Exception as e:
            print(f"Error fetching buttons: {str(e)}")
            return []


# ТЕСТ Функция для генерации клавиатуры - Кнопки через API
async def fetch_buttons_from_api_TEST(endpoint_id: int):
    response = {
        "buttons": [
            {
                "id": 101,
                "name": "Презентация компании",
                "url": "https://example.com/presentation"
            },
            {
                "id": 102,
                "name": "Карточка компании",
                "url": "https://example.com/card"
            }
        ]
    }
    # Возвращаем список кнопок из ответа API без вызова .json()
    return response.get('buttons', [])


# Генерация клавиатуры на основе данных из API
async def generate_keyboard(buttons_data):
    # Создаем пустой список для хранения строк с кнопками
    inline_keyboard = []

    # Заполняем строки кнопками
    for button in buttons_data:
        if button.get('url'):
            # Если у кнопки есть URL, создаем кнопку-ссылку
            inline_keyboard.append([
                InlineKeyboardButton(
                    text=button['name'],
                    url=button['url']
                )
            ])
        else:
            # Иначе создаем callback-кнопку для обработки нажатия
            inline_keyboard.append([
                InlineKeyboardButton(
                    text=button['name'],
                    callback_data=f"callback_{button['id']}"
                )
            ])

    # Создаем объект InlineKeyboardMarkup с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return keyboard
