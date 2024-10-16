from api.api_handlers import get_api_data, post_api_data
from keyboards.contact_request import ContactViaType

async def manager_login_with_tg_id(tg_id: int) -> dict[str, str]:
    return await post_api_data(
        endpoint="auth/get_user-jwf-by-tg-id",
        data={ 'tg_id': tg_id }
    )


async def get_all_orders_for_manager(
    jwt: str,
    in_progress: bool,
    for_user: bool
):
    headers = {
        "accept": "application/json",
        "Authorization": jwt
    }
    params = {
        "for_current_user": str(for_user),
        "is_processed": 'False',
        "in_progress": str(in_progress),
    }
    return await get_api_data(
            endpoint=f"contact_requests/all",
            params=params,
            headers=headers
        )


async def set_order_to_work(
    jwt: str,
    order_id: int,
    manager_tg_id: int
):
    headers = {
        "accept": "application/json",
        "Authorization": jwt
    }
    data = {
        'managet_telegram_id': str(manager_tg_id)
    }
    return await post_api_data(
            endpoint=f"contact_requests/{order_id}/take-to-work",
            headers=headers,
            data=data
        )


async def close_order(
    jwt: str,
    order_id: int
):
    headers = {
        "accept": "application/json",
        "Authorization": jwt
    }
    return await post_api_data(
        endpoint=f"contact_requests/{order_id}/close-request",
        headers=headers
    )


async def create_contact_request(
    state_data: dict
):
    headers = {
        "accept": "application/json"
    }
    json = {
        "telegram_user_id": str(state_data["current_user_id"]),
        "name": state_data["current_user_username"],
        "phone": state_data["phone"] if state_data["phone"] else "не указан",
        "email": state_data["email"] if state_data["email"] else "не указан",
        "text": state_data["question"],
        "contact_via_telegram": (
            state_data["contact_via_type"] == ContactViaType.tg
        ),
        "contact_via_phone": (
            state_data["contact_via_type"] == ContactViaType.phone
        ),
        "contact_via_email": (
            state_data["contact_via_type"] == ContactViaType.email
        )
    }
    return await post_api_data(
        endpoint=f"contact_requests",
        headers=headers,
        json=json
    )