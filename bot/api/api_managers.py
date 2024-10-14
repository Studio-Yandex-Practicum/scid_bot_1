from api.api_handlers import get_api_data, post_api_data


async def manager_login_with_tg_id(tg_id: int) -> dict[str, str]:
    return await post_api_data(
        endpoint="auth/get_user-jwf-by-tg-id",
        data={ 'tg_id': tg_id }
    )


async def get_all_orders_for_manager(
    jwt: str,
    in_progress: bool,
):
    headers = {
        "accept": "application/json",
        "Authorization": jwt
    }
    params = {
        "for_current_user": 'True',
        "is_processed": 'False',
        "in_progress": str(in_progress),
    }
    return await get_api_data(
            endpoint=f"contact_requests/all",
            params=params,
            headers=headers
        )