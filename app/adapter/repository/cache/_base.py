from redis import StrictRedis
from redis.client import Pipeline
from app.abc.repository.base import Repository


class RedisRepository(Repository):
    __repo_name__: str = "base"
    prefix: str = ""

    def __init__(self, conn: StrictRedis | Pipeline):
        self.conn: StrictRedis | Pipeline = conn