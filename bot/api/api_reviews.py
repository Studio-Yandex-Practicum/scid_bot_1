from api.api_handlers import post_api_data

REVIEWS_COMMON_URL = "reviews"

async def handle_reviews_create(
    user_id: int,
    review_text: str,
    rating: int
):
    headers = {
        "accept": "application/json"
    }
    data = {
        "telegram_user_id": str(user_id),
        "text": review_text,
        "rating": rating
    }
    return await post_api_data(
            endpoint=f"{REVIEWS_COMMON_URL}/",
            headers=headers,
            json=data
        )