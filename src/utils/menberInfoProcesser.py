import json
import time

import requests

url = 'https://psync.48.cn/syncsystem/api/cache/v1/update/overview'

header = {
    'os': 'android',
    'Content-type': 'application/json',
    'version': '5.0.1'
}

data = {
    "videoTypeUtime": "2017-03-24 15:59:11",
    "musicAlbumUtime": "2017-04-18 14:45:37",
    "functionUtime": "2017-10-17 15:00:00",
    "groupUtime": "2017-10-17 17:27:00",
    "memberInfoUtime": "2017-10-20 11:55:09",
    "talkUtime": "2017-05-05 18:04:52",
    "videoUtime": "2017-05-17 18:36:32",
    "musicUtime": "2017-05-05 15:56:11",
    "urlUtime": "2017-07-19 12:10:59",
    "teamUtime": "2017-10-20 10:39:00",
    "memberPropertyUtime": "2017-02-20 18:57:48",
    "periodUtime": "2017-10-14 14:45:00"
}
resp = requests.post(url, json=data, headers=header)
resp.encoding = 'utf-8'
# print(resp.json())
# exit()
memberinfo = resp.json()

roomInfo = dict()

# exit()

for member in memberinfo['content']['memberInfo']:
    if str(member['city']) == '12':
        roomInfo[member['member_id']] = member['real_name']

print(str(roomInfo))

try:
    file = open('./memberinfo.py', 'w', encoding='utf-8')
    file.write('members='+str(roomInfo))
    # file.flush()
finally:
    if file:
        file.close()
