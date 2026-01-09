import logging
import uuid

import db
from gps_reader import read_gps_data

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    db.init_send_queue_db()
    tour_id = str(uuid.uuid4())
    logger.info("ツーリング開始 ツーリングID: %s", tour_id)

    read_gps_data(tour_id)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("キーボード割り込み")
    except Exception:
        logger.exception("ハンドルされていない例外")
        raise
