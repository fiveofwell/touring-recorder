import serial
import time
import logging

import settings
import db
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
running = True

def convert_date(utc, date):
    try:
        if not utc or not date:
            raise ValueError("empty")

        hour = int(utc[0:2])
        minute = int(utc[2:4])
        second = int(utc[4:6])

        frac = utc[7:] if len(utc) > 7 else "0"
        millisecond = int(float("0." + frac) * 1000000)

        day = int(date[0:2])
        month = int(date[2:4])
        year = int("20" + date[4:6])

        return datetime(year, month, day, hour, minute, second, millisecond, tzinfo=timezone.utc)

    except Exception:
        logger.warning("不正な時刻データ utc=%s date=%s", utc, date)
        return None


def convert_nmea(val):
    degree = int(val / 100)
    minutes = val - degree * 100
    return degree + minutes / 60


def stop():
    global running
    running = False


def connect():
    while True:
        try:
            logger.info("GPS接続試行")
            return serial.Serial(
                settings.SERIAL_PORT,
                settings.BAUDRATE,
                timeout=settings.READ_TIMEOUT_SEC
            )
        except Exception as e:
            logger.error("GPS接続失敗: %s", e)
            time.sleep(2)


def read_gps_data(tour_id):
    serial_port = None

    try:
        now = time.monotonic()
        next_enqueue = now
        next_send = now
        flow_control = 1

        serial_port = connect()
        logger.info("GPS接続成功")

        while running:
            try:
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
    
                try:
                    latitude = convert_nmea(float(fields[3]))
                    if fields[4] == 'S':
                        latitude = -latitude
        
                    longitude = convert_nmea(float(fields[5]))
                    if fields[6] == 'W':
                        longitude = -longitude
            
                except (ValueError, IndexError) as e:
                    logger.warning("不正なGPSデータ: %s", line)
                    continue

                timestamp = convert_date(fields[1], fields[9])
                if timestamp is None:
                    continue
                logger.debug("GPS:%.6f,%.6f,%s",latitude, longitude, timestamp)
    
                db.enqueue_data(tour_id, latitude, longitude, timestamp)
                next_enqueue = now + settings.STORE_INTERVAL_SEC
    
            except serial.SerialException as e:
                logger.error("Serial error: %s", e)

                logger.error("GPS切断検知、再接続します")

                serial_port.close()
                serial_port = connect()
                logger.info("GPS再接続成功")
                flow_control = 1
                continue

            except Exception:
                logger.exception("GPSループ内例外")
                time.sleep(2)
                continue
    
    except KeyboardInterrupt:
        pass

    finally:
        if serial_port:
            serial_port.close()
