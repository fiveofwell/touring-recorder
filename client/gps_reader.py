import serial
import time
import logging

import settings
import db
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def convert_date(utc, date):
    if not utc or not date:
        return datetime.now(timezone.utc)

    #hhmmss.ss
    hour = int(utc[:2])
    minute = int(utc[2:4])
    second = int(utc[4:6])
    millisecond = int(float("0." + utc[7:]) * 1000000)

    #ddmmyy
    day = int(date[:2])
    month = int(date[2:4])
    year = int("20" + date[4:])
    return datetime(year, month, day, hour, minute, second, millisecond, tzinfo=timezone.utc)


def convert_nmea(val):
    degree = int(val / 100)
    minutes = val - degree * 100
    return degree + minutes / 60


def read_gps_data(tour_id):
    serial_port = None

    try:
        now = time.monotonic()
        next_enqueue = now
        next_send = now
        flow_control = 1

        serial_port = serial.Serial(
            settings.SERIAL_PORT,
            settings.BAUDRATE,
            timeout=settings.READ_TIMEOUT_SEC
        )

        while True:
            data = serial_port.readline()
            line = data.decode('ascii', errors='ignore').strip()
            now = time.monotonic()

            if now >= next_send:
                status = db.dequeue_data()
                if status == "sent":
                    flow_control = 1
                elif status == "fail":
                    flow_control = min(flow_control * 2, settings.MAX_FLOW_CONTROL)
                next_send += settings.FLUSH_INTERVAL_SEC * flow_control

            if now < next_enqueue:
                continue
            
            if not line.startswith("$GPRMC"):
                continue

            fields = line.split(',')
            if len(fields) < 13 or fields[2] != 'A':
                continue

            latitude = convert_nmea(float(fields[3]))
            if fields[4] == 'S':
                latitude = -latitude

            longitude = convert_nmea(float(fields[5]))
            if fields[6] == 'W':
                longitude = -longitude

            timestamp = convert_date(fields[1], fields[9])
            logger.debug("GPS:%.6f,%.6f,%s",latitude, longitude, timestamp)

            db.enqueue_data(tour_id, latitude, longitude, timestamp)
            next_enqueue = now + settings.STORE_INTERVAL_SEC


    except KeyboardInterrupt:
        pass

    finally:
        if serial_port:
            serial_port.close()