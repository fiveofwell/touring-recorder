import redis
from fastapi import HTTPException, status

def get_redis_client():
    try:
        client = redis.Redis(host='redis', decode_responses=True, socket_connect_timeout=5)
        client.ping()
        return client
    except (redis.ConnectionError, redis.TimeoutError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis service unavailable",
        )