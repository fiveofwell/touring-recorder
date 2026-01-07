import requests
import settings
import logging

logger = logging.getLogger(__name__)

def start_tour():
    try:
        headers = {'X-API-Key': settings.X_API_KEY}
        response = requests.get(settings.TOUR_START_URL, headers=headers, timeout=settings.POST_TIMEOUT_SEC)

        if response.status_code == 200:
            tour_id = response.json()["tour_id"]
            logger.info("ツーリングID発行")
            return tour_id 

        logger.warning("ツーリングID発行失敗:%d", response.status_code)
        return None

    except requests.exceptions.RequestException:
        logger.warning("ツーリングID発行失敗")
        return None

    except Exception:
        logger.exception("ハンドルされていない例外")
        return None


def post_gps_data(tour_id, points):
    headers = {'X-API-Key': settings.X_API_KEY}
    payload = {
        "tour_id": tour_id,
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
        return response.json()["accepted_ids"]

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            logger.warning("HTTPエラー:%d", e.response.status_code)
        return None

    except requests.exceptions.RequestException:
        logger.warning("データ送信失敗")
        return None