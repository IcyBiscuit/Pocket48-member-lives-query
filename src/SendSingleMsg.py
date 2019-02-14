import asyncio
import random
# import liveUtils
import time

import uvloop

from utils.LiveUtils import LiveUtil

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


liveUtil = LiveUtil(needRedis=False)

loop = asyncio.get_event_loop()

text = '快放了我 呜呜呜呜呜\n ┭┮﹏┭┮'


test_msg = 'test_msg_%d' % (time.time_ns()//1000)

msg = liveUtil.send(685774008, text)

resp = loop.run_until_complete(msg)
print(resp)
