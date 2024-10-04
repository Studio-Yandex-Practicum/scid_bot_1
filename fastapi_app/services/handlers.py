from fastapi_app.services.request import (
    post_api_data,
    get_api_data,
    patch_api_data,
    delete_api_data,
)


# bot_menu
BOT_MENU_COMMON_URL = '/api/bot-menu'


async def handle_menu_get_main_menu_button():
    return await get_api_data(
        f'{BOT_MENU_COMMON_URL}/get-main-menu-button', {}
    )


async def handle_menu_get_content(button_id):
    return await get_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/get-content', {}
    )


async def handle_menu_get_image(button_id):
    return await get_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/get-image-file', {}
    )


async def handle_menu_get_child_buttons(button_id):
    return await get_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/get-child-buttons', {}
    )


async def handle_menu_add_child_button(button_id):
    return await post_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/add-child-button', {}
    )


async def handle_menu_change_parent(button_id):
    return await patch_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/change_parent', {}
    )


async def handle_menu_button_update(button_id):
    return await patch_api_data(f'{BOT_MENU_COMMON_URL}/{button_id}', {})


async def handle_menu_delete_child_button(button_id):
    return await delete_api_data(f'{BOT_MENU_COMMON_URL}/{button_id}', {})


async def handle_menu_add_files(button_id):
    return await post_api_data(f'{BOT_MENU_COMMON_URL}/{button_id}/files', {})


async def handle_menu_get_files(button_id):
    return await get_api_data(f'{BOT_MENU_COMMON_URL}/{button_id}/files', {})


async def handle_menu_delete_files(button_id):
    return await delete_api_data(
        f'{BOT_MENU_COMMON_URL}/{button_id}/files', {}
    )


# auth
async def handle_auth_login():
    return await post_api_data('api/auth/jwt/login', {})


async def handle_auth_logout():
    return await post_api_data('api/auth/jwt/logout', {})


async def handle_auth_reset_password():
    return await post_api_data('api/auth/reset-password', {})


async def handel_auth_me():
    return await patch_api_data('api/auth/me', {})


# contact_request
async def handle_contact_request():
    return await post_api_data('api/contact-request', {})
