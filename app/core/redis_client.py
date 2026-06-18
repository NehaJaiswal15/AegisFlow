import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=2,  # db0 = Celery broker, db1 = Celery results, db2 = our cache
    decode_responses=True,  # Returns strings instead of bytes
)
