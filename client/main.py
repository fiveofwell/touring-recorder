import logging
import uuid
import signal
import sys

import db
from gps_reader import read_gps_data, stop
from db import dequeue_data

logger = logging.getLogger(__name__)

def shutdown_handler(signum, frame):
    logger.info("SIGTERM受信、記録を終了します")
    stop()

    max_flush = 10
    status = "sent"
    count = 0

    while status == "sent" and count < max_flush:
        status = dequeue_data()
        count += 1

    if status == "empty":
        logger.info("flush成功")
    elif status == "fail":
        logger.info("flush失敗、次回起動時送信します")
    else:
        logger.info("flush中断、次回起動時送信します")

    sys.exit(0)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

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
