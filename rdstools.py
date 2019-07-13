import redis

URL = "redis://@127.0.0.1:6379/5"
READ_COUNT = "article:readcount:%s"
client = redis.StrictRedis().from_url(URL)

