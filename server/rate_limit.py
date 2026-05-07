from fastapi import Depends, status, HTTPException, Request
import redis
from redis_client import get_redis_client

def get_client_ip(request: Request):
    # Cloudflareのプロキシの場合
    cf_connecting_ip = request.headers.get('CF-Connecting-IP')
    if cf_connecting_ip:
        return cf_connecting_ip
    
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip
    
    if request.client:
        return request.client.host
    
    return "unknown"


def rate_limit(
    limit: int = 100,
    window: int = 60
):
    async def limiter(
        request: Request,
        redis_client: redis.Redis = Depends(get_redis_client)
    ):
        ip = get_client_ip(request)
        key = f"rate_limit:{ip}:{request.url.path}"

        count = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key, window)
        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
                headers={"Retry-After": str(window)}
            )
    return limiter
