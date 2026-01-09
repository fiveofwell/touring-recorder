import requests
import settings
import logging

logger = logging.getLogger(__name__)

def post_gps_data(tour_id, points):
    headers = {'X-API-Key': settings.X_API_KEY}
    payload = {
        "device_id": settings.device_id,
        "points": points,
    }

    try:
        response = requests.post(
            settings.API_URL,
            headers=headers,
            json=payload,
            timeout=settings.POST_TIMEOUT_SEC
        )

        response.raise_for_status()
        return response.json()["ok"]

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            logger.warning("HTTPエラー:%d", e.response.status_code)
        return None

    except requests.exceptions.RequestException:
        logger.warning("データ送信失敗")
        return None