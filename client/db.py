import sqlite3
import logging
from datetime import datetime, timezone
import settings
import api_client

logger = logging.getLogger(__name__)

def init_send_queue_db():
    with sqlite3.connect(settings.DBNAME) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS gps_send_queue(queue_id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, device_id TEXT, latitude REAL, longitude REAL, timestamp TEXT)')

        # 送信キューにデータが残っているかもしれないので起動時にFlush
        cur.execute('DELETE FROM gps_send_queue')


def dequeue_data(tour_id):
    with sqlite3.connect(settings.DBNAME) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            'SELECT queue_id, device_id, latitude, longitude, timestamp FROM gps_send_queue ORDER BY queue_id LIMIT ?',
            (settings.SEND_LIMIT,)
        )

        rows = cur.fetchall()
        points = [dict(row) for row in rows]

        if len(points) == 0:
            return "empty"

        accepted_ids = api_client.post_gps_data(tour_id, points)

        if accepted_ids is None:
            return "fail"

        if not accepted_ids:
            return "empty"

        placeholders = ",".join("?" for _ in accepted_ids)
        sql = f'DELETE FROM gps_send_queue WHERE queue_id IN ({placeholders})'

        cur.execute(sql, accepted_ids)
        conn.commit()

        logger.info("送信成功:%d件", len(accepted_ids))
        return "sent" 


def enqueue_data(latitude, longitude, timestamp):
    with sqlite3.connect(settings.DBNAME) as conn:
        cur = conn.cursor()

        values = (
            datetime.now(timezone.utc),
            settings.DEVICE_ID,
            latitude,
            longitude,
            timestamp
        )
        sql = 'INSERT INTO gps_send_queue (created_at, device_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?, ?)'

        cur.execute(sql, values)
        conn.commit()
