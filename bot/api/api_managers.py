from api.api_handlers import get_api_data, post_api_data


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