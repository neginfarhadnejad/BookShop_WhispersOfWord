import redis

redis_client = redis.Redis(
    host="localhost",  # یا آدرس داکر سرویس ردیس
    port=6379,
    db=0,
    decode_responses=True
)
