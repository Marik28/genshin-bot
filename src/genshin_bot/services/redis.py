from redis import Redis

from ..settings import settings

redis = Redis(
    settings.redis_host,
    settings.redis_port,
    settings.redis_db,
    decode_responses=True,
)
