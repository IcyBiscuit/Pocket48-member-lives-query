import asyncio
import random
import time
from sys import argv

import uvloop

from configs.groupsConfig import groups
from configs.memberInfo import members
from utils.LiveUtils import LiveUtil

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PushService:

    def __init__(self, redisPassword=None, args=None):
        self.mode = args
        print('service started mode: %s' % (self.mode))
        self.liveUtil = LiveUtil(needRedis=True, redisPassword=redisPassword)

    def schedule(self):

        liveSet = set()
        preSet = set()

        while True:
            try:
                liveList = self.liveUtil.getGNZMenberLive(members)
            except Exception:
                time.sleep(60)

            msg = ''
            for live in liveList:
                if str(live) not in preSet:
                    msg = msg+self.liveUtil.buildLiveMessageString(live)
                liveSet.add(str(live))
            # print(msg)

            # if msg and msg != '':
            #     print(msg)
            # elif msg == '' and self.mode == 'debug':
            # if (not msg or msg == '')and self.mode == 'debug':
            #     msg = ('秃头组女装激情调试中... empty live list set_' +
            #            str(time.time_ns()//1000))
            if msg and msg != '':
                try:
                    self.pushMsg(msg)
                    preSet.clear()
                    preSet = liveSet.copy()
                    liveSet.clear()
                except Exception:
                    print('messages push exception')
                    time.sleep(120)
                    continue

            # print(preSet)
            time.sleep(random.randint(30, 45))

    def pushMsg(self, msg):
        loop = asyncio.get_event_loop()
        tasks = []
        for groupId in groups:
            tasks.append(self.liveUtil.send(groupId, msg))
        loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    redisPassword = None
    if len(argv) > 1:
        redisPassword = argv[1]
        # args = argv[2]
    PushService(redisPassword=redisPassword).schedule()
