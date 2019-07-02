import redis

URL = "your redis url"
READ_COUNT = "article:readcount:%s"
client = redis.StrictRedis().from_url(URL)

