from api.api_service import get_child_buttons


def format_text(data, prefix="", is_last=True):
    result = ""
    for index, item in enumerate(data):
        # Определяем, последний ли это элемент на уровне
        current_prefix = prefix + ("└── " if index == len(data) - 1 else "├── ")
        # Формируем строку для текущего элемента
        result += f"{current_prefix}{item['label']} ({item['id']})\n"
        # Добавляем префикс для следующего уровня
        child_prefix = prefix + ("    " if index == len(data) - 1 else "|   ")        
        # Рекурсивно обрабатываем дочерние элементы
        children = item.get("children", [])
        if children:
            result += format_text(children, child_prefix, True)
    return result

async def render_recursive(button_id):    
    child_buttons = await get_child_buttons(button_id)    
    for button in child_buttons:
        button["children"] = await render_recursive(button["id"])
    return child_buttons