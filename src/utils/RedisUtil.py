import redis

from configs.memberInfo import members


class RedisUtil:
    def __init__(self, host='localhost', password=None, port=6379):

        self.keyName = 'LiveNicknames'
        self.redisConfig = {
            'host': host,
            'port': port,
            'password': password
        }

        # connections = redis.Connection(host='127.0.0.1', password=password)
        # pool = redis.ConnectionPool(connection_class=connections)
        pool = redis.ConnectionPool(
            host=self.redisConfig['host'], port=self.redisConfig['port'], password=self.redisConfig['password'])
        # self.r = redis.Redis('127.0.0.1', password=password)
        self.r = redis.StrictRedis(connection_pool=pool)
        if not self.r.exists(self.keyName):
            # print('loading member info into redis')
            # pipeline = self.r.pipeline()
            # for roomId, nickname in members.items():
            #     pipeline.hset(self.keyName, roomId, nickname)
            # pipeline.execute()
            self.initNicknames()

    def getMemberNickname(self, memberId):
        try:
            if not self.r.exists(self.keyName):
                self.initNicknames()
            nickname = self.r.hget(self.keyName, memberId).decode()
        except Exception:
            nickname = ''
        if not nickname or nickname == ''or nickname == 0:
            return members[memberId]
        return nickname

    def isContains(self, memberId):
        return self.r.hexists(self.keyName, memberId)

    def initNicknames(self):
        pipeline = self.r.pipeline()
        for roomId, nickname in members.items():
            pipeline.hset(self.keyName, roomId, nickname)
        # pipeline.expire(self.keyName, 24*3600)
        pipeline.execute()


if __name__ == "__main__":
    redisutil = RedisUtil()
    print(redisutil.getMemberNickname(63548))
