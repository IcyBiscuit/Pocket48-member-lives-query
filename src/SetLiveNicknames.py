import redis

from configs.memberInfo import members
from configs.redisConfig import configs

redisConfig = configs['remotehost']


# pool = redis.ConnectionPool(
#     host=redisConfig['host'], port=redisConfig['port'], password=redisConfig['password'])

# r = redis.Redis('127.0.0.1', port=6379, password=None)
r = redis.StrictRedis(
    host=redisConfig['host'], port=redisConfig['port'], password=redisConfig['password'])

key = 'LiveNicknames'
pipeline = r.pipeline()

for memberId, nicknames in members.items():
    pipeline.hset(key, memberId, nicknames)
    # print('setting member: %d, nickname: %s... returns %d' %
    #       (memberId, nicknames, returns))
try:
    resp = pipeline.execute()
    print(resp)
    # print(r.hgetall(key))
except Exception:
    print('exception caught')
