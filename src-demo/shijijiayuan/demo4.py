import requests
from multiprocessing.dummy import Pool as ThreadPool
import re
import time
global s

def getUID(pageNum, cookies):
    global s
    time.sleep(0.3)
    url = 'http://search.jiayuan.com/v2/search_v2.php'
    payload = {'sex': 'f',
               'key': '',
               'stc': '23:1',
               'sn': 'default',
               'sv': '1',
               'p': pageNum,
               'f': 'select',
               'listStyle': 'bigPhoto',
               'pri_uid': 0,
               'jsversion': 'v5'}
    # headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    #            'Referer': 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=23:1&sn=default&sv=1&p=1&pt=67848&ft=off&f=select&mt=d',
    #            'X-Requested-With': 'XMLHttpRequest'}
    r = s.post(url, data=payload, cookies=cookies)
    pattern = '"userInfo":\[(.*?)\]'
    content = re.findall(pattern, r.text)[0]
    pattern = '"realUid":(\d+),'
    uidList = re.findall(pattern, content)
    return [uidList, r.cookies]

s = requests.session()
print(s)
login_data = {'name': 'sjjy_a@sina.com', 'password': 'tobeyourself1314'}
url = "https://passport.jiayuan.com/dologin.php?pre_url=http://usercp.jiayuan.com/"
a = s.post(url, login_data)
print(a.text)

uid = []

cookies = {}
for i in range(1, 200):
    result = getUID(i, cookies)
    uid = uid + result[0]
    cookies = result[1]

print(len(uid))
print(len(set(uid)))

# print(s.post("http://www.jiayuan.com/127701554").text)

