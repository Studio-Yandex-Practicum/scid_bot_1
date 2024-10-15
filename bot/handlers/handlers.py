from bot.api.api_handlers import (delete_api_data, get_api_data,
                                  patch_api_data, post_api_data)

BOT_MENU_COMMON_URL = "/api/bot-menu"
AUTH_COMMON_URL = "/api/auth"
CONTACT_REQUESTS_COMMON_URL = "/api/contact-requests"
REVIEWS_COMMON_URL = "/api/reviews"


# bot_menu
async def handle_menu_get_main_menu_button():
    return await get_api_data(
        f"{BOT_MENU_COMMON_URL}/get-main-menu-button", {}
    )


async def handle_menu_get_content(button_id):
    return await get_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/get-content", {}
    )


async def handle_menu_get_image(button_id):
    return await get_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/get-image-file", {}
    )


async def handle_menu_get_child_buttons(button_id):
    return await get_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/get-child-buttons", {}
    )


async def handle_menu_add_child_button(button_id):
    return await post_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/add-child-button", {}
    )


async def handle_menu_change_parent(button_id):
    return await patch_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/change_parent", {}
    )


async def handle_menu_button_update(button_id):
    return await patch_api_data(f"{BOT_MENU_COMMON_URL}/{button_id}", {})


async def handle_menu_delete_child_button(button_id):
    return await delete_api_data(f"{BOT_MENU_COMMON_URL}/{button_id}", {})


async def handle_menu_add_files(button_id):
    return await post_api_data(f"{BOT_MENU_COMMON_URL}/{button_id}/files", {})


async def handle_menu_get_files(button_id):
    return await get_api_data(f"{BOT_MENU_COMMON_URL}/{button_id}/files", {})


async def handle_menu_delete_files(button_id):
    return await delete_api_data(
        f"{BOT_MENU_COMMON_URL}/{button_id}/files", {}
    )


# auth
async def handle_auth_login():
    return await post_api_data(f"{AUTH_COMMON_URL}/jwt/login", {})


async def handle_auth_logout():
    return await post_api_data(f"{AUTH_COMMON_URL}/jwt/logout", {})


async def handle_auth_forgot_password():
    return await post_api_data(f"{AUTH_COMMON_URL}/forgot-password", {})


async def handle_auth_reset_password():
    return await post_api_data(f"{AUTH_COMMON_URL}/reset-password", {})


async def handel_auth_me():
    return await patch_api_data(f"{AUTH_COMMON_URL}/me", {})


# contact_request
async def handle_contact_requests_create():
    return await post_api_data(f"{CONTACT_REQUESTS_COMMON_URL}/", {})


async def handle_contact_requests_get_all():
    return await get_api_data(f"{CONTACT_REQUESTS_COMMON_URL}/all", {})


async def handle_contact_requests_get(request_id):
    return await get_api_data(
        f"{CONTACT_REQUESTS_COMMON_URL}/{request_id}", {}
    )


async def handle_contact_requests_patch(request_id):
    return await patch_api_data(
        f"{CONTACT_REQUESTS_COMMON_URL}/{request_id}", {}
    )


async def handle_contact_requests_delete(request_id):
    return await delete_api_data(
        f"{CONTACT_REQUESTS_COMMON_URL}/{request_id}", {}
    )


# reviews
async def handle_reviews_create():
    return await post_api_data(f"{REVIEWS_COMMON_URL}/", {})


async def handle_reviews_get_all():
    return await get_api_data(f"{REVIEWS_COMMON_URL}/", {})


async def handle_reviews_count():
    return await get_api_data(f"{REVIEWS_COMMON_URL}/count", {})


async def handle_reviews_average_rating():
    return await get_api_data(f"{REVIEWS_COMMON_URL}/average-rating", {})


async def handle_reviews_get(review_id):
    return await get_api_data(f"{REVIEWS_COMMON_URL}/{review_id}", {})


async def handle_reviews_delete(review_id):
    return await delete_api_data(f"{REVIEWS_COMMON_URL}/{review_id}", {})
