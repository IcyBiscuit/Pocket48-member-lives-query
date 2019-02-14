import asyncio
import time

import aiohttp
import uvloop

from configs.liveType import liveType
from utils.RedisUtil import RedisUtil

# from configs.memberInfo import members as memberList

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class LiveUtil:
    def __init__(self, needRedis=True, redisPassword=None):
        # if needRedis:
        self.redisUtil = RedisUtil(password=redisPassword)

    def getGNZMenberLive(self, memberList):

        loop = asyncio.get_event_loop()
        liveList = loop.run_until_complete(self.getLiveList())

        # liveList = self.getLiveList()
        returnList = list()

        if liveList and liveList != '':
            for live in liveList:
                # print(live)
                try:
                    memberId = live['memberId']
                    # if memberList.__contains__(memberId):
                    if (memberId in memberList)or self.redisUtil.isContains(memberId):
                        liveInfo = self.pharseLiveInfo(live)
                        # print(liveInfo)
                        returnList.append(liveInfo)
                except Exception:
                    print('成员Id解析出错')
                    pass
        return returnList

    async def getLiveList(self):
        url = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'

        header = {
            'Content-type': 'application/json',
            'version': '5.0.1',
            'os': 'Android'
        }

        data = {
            "lastTime": 0,
            "limit": 5,
            "memberId": 0,
            "groupId": 0,
            "giftUpdTime": 1503766100000
        }

        # session = requests.session()
        # resp = session.post(url, headers=header, json=data)
        liveList = ''

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30), connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=header, json=data) as resp:
                try:
                    respJSON = await resp.json()
                    liveList = respJSON['content']['liveList']
                    # print(liveList)
                except Exception:
                    print('live list JSON parse error')
        return liveList

    def getLiveId(self, live):
        try:
            liveId = live['liveId']
        except Exception:
            print("live info pharse error")
            pass
        return liveId

    async def getLiveOne(self, liveId):

        header = {
            'Content-type': 'application/json',
            'version': '5.0.1',
            'os': 'Android'
        }

        # url = 'https://plive.48.cn/livesystem/api/live/v1/getLiveOne'
        url = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30), connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=header, json={
                    "type": 1,
                    "userId": 0,
                    "liveId": str(liveId)
            }) as resp:
                try:
                    json = await resp.json()
                    # print(json)
                    return json
                except Exception:
                    print("get live one json parse error")
                    return

    def pharseLiveInfo(self, live):
        try:
            memberId = live['memberId']
            liveInfo = {
                'memberId': memberId,
                # 'name': (str(live['title']).split('的', 1))[0],
                # 'name': '%s' % (memberList[live['memberId']]),
                'name': '%s' % (self.redisUtil.getMemberNickname(memberId)),
                'title': live['subTitle'],
                'type': live['liveType'],
                'liveId': live['liveId'],
                'streamPath': live['streamPath'],
                'startTime': live['startTime']
            }
            return liveInfo
        except Exception:
            print('成员直播信息解析出错\nLive: %s' % (live))
            pass

    def buildLiveMessageString(self, liveInfo):

        msg = "\n%s的%s: %s\n流地址:\n%s\n开始时间: %s\n" % (
            liveInfo['name'],
            liveType[liveInfo['type']],
            liveInfo['title'], liveInfo['streamPath'],
            time.strftime("%m/%d %H:%M",
                          time.localtime(liveInfo['startTime']/1000)))
        return msg

    async def send(self, groupId, message):
        # url = 'http://120.78.167.103:5700/send_group_msg'
        url = 'http://120.78.167.103:5700/send_group_msg?access_token=ztrobot2018'

        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data={
                'group_id': groupId,
                'message': message
            }) as resp:
                try:
                    respText = await resp.json()
                    return respText
                except Exception:
                    print('解析响应JSON异常')
                    return resp
