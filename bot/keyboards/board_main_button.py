from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def make_main_button_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    """
    items: список словарей, где каждый элемент содержит 'text' и 'url'
    Пример: [{"text": "Google", "url": "https://google.com"}, {"text": "Yandex", "url": "https://yandex.ru"}]
    """
    # Создаем клавиатуру
    keyboard = InlineKeyboardMarkup()

    # Проходим по каждому элементу из списка
    for item in items:
        # Создаем кнопку с текстом и url
        button = InlineKeyboardButton(text=item['text'], url=item['url'])
        # Добавляем кнопку в клавиатуру
        keyboard.add(button)

    return keyboard
