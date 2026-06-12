import requests
import logging
import urllib.parse as urlparse

import settings

logger = logging.getLogger(__name__)

def post_gps_data(tour_id, points):
    headers = {'X-API-KEY': settings.X_API_KEY}
    payload = {
        "points": points,
    }

    try:
        api_url = f"{settings.API_URL}/{tour_id}/points"

        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=settings.POST_TIMEOUT_SEC
        )

        response.raise_for_status()
        return response.json()["ok"]

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            logger.warning("HTTPエラー:%d", e.response.status_code)
            logger.warning("HTTPエラー:%s", e.response.text)
        return None

    except requests.exceptions.RequestException:
        logger.warning("データ送信失敗")
        return None
