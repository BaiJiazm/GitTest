# -*- coding:utf-8 -*-
import urllib.request as urllib2
import requests
from bs4 import BeautifulSoup
import random
import time
import sys
import os
import urllib3

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

hrefFile = open("run1Href.txt", "w")
resFile = open("run1Res.txt", "w")

proxyHandler = urllib2.ProxyHandler({
    'http': 'http://115.225.88.99:8118',
    'http': 'http://118.190.95.43:9001',
    'http': 'http://111.155.116.207:8123',
    'http': 'http://122.114.31.177:808',
    'http': 'http://106.56.102.254:8070',
    'http': 'http://111.155.116.249:8123',
    'http': 'http://180.118.240.8:61234',
    'http': 'http://60.177.225.218:18118'
})

opener = urllib2.build_opener(proxyHandler)
urllib2.install_opener(opener)

prefix = 'https://www.tvmao.com'
postUrl = 'https://www.tvmao.com/program/duration/'
todoUrlSet = {
    # '/program/CCTV'
    '/program/HEBEI'
}
doneUrlSet = set()
channelsSet = set()

# userAgents是爬虫与反爬虫斗争的第一步
userAgents = ['User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
              'User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
              'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
              'User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;InfoPath.2;.NET4.0C;.NET4.0E;.NETCLR2.0.50727;360SE',
              'User-Agent:Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
              'User-Agent:Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11 ',
              'User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50 ',
              'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1660.400'
              ]

header = {}
header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
header['Accept-Encoding'] = 'gzip, deflate, br'
header['Accept-Language'] = 'zh-CN,zh;q=0.9'
header['Connection'] = 'keep-alive'
# header['Content-Length'] = '6'
# header['Content-Type'] = 'aapplication/x-www-form-urlencoded'
# header['Host'] = 'www.tvmao.com'
# header['Origin'] = 'https://www.tvmao.com'
# header['Referer'] = 'https://www.tvmao.com/program/channelsSet/'
header['User-Agent'] = ''
# header['Cache-Control'] = 'max-age=0'
# header['Upgrade-Insecure-Requests'] = '1'


def getHeaders():
    # 随机获取一个headers
    # headers = {'User-Agent': random.choice(userAgents)}
    header['User-Agent'] = random.choice(userAgents)
    return header


def parseHtml(html):
    # print(html)
    div = BeautifulSoup(html,  "lxml").find_all('div', class_='chlsnav')
    divBs = BeautifulSoup(str(div),  "lxml")
    # print(divBs.prettify())

    ul = divBs.ul.extract()
    # print(BeautifulSoup(str(ul),  "lxml").prettify)
    # print(BeautifulSoup(str(divBs),  "lxml").prettify)
    # sys.stdout.flush()
    # os._exit(0)

    # 寻找可能的新链接页面
    allA = divBs.find_all('a')
    for each in allA:
        href = each['href']
        if (href not in doneUrlSet) and (href not in todoUrlSet):
            print(each.string, href)
            print(each.string, href, file=hrefFile)
            todoUrlSet.add(str(href))

    # 搜集未发现的节目
    # 查找当前频道仅为了结果的顺序更好一些
    curChn = ul.find_all('li', class_='curchn')
    # print(curChn)
    for each in curChn:
        chn = each.string
        if chn not in channelsSet:
            print(chn)
            print(chn, file=resFile)
            channelsSet.add(chn)

    a = ul.find_all('a')
    # print(a)
    for each in a:
        chn = each.string
        if chn not in channelsSet:
            print(chn)
            print(chn, file=resFile)
            channelsSet.add(chn)


def spiderGet(url):
    response = requests.get(url=url, headers=getHeaders(), verify=False)
    response.encoding = 'utf-8'
    parseHtml(html=response.text)


# def spiderPost(option):
#     data = {'prov': '130000'}
#     # header['Content-Length'] = str(5+len(option))
#     header['Content-Length'] = '11'
#     header['Content-Type'] = 'aapplication/x-www-form-urlencoded'
#     header['Cookie'] = 'UM_distinctid=164915db395f1-073fb37f3c265b-4d754111-1fa400-164915db39688f; _ga=GA1.2.608139993.1531447194; _gid=GA1.2.275641975.1531711461; __cfduid=d54070043b548b24c3ca227d042f495591531712204; Hm_lvt_a27d3c53126c59f93b8f63a30262cb5e=1531447194,1531463385,1531712204; JSESSIONID=abcKK8WT_JJU84LkHmHsw; ASCK=; CNZZDATA1255238971=113633666-1531444173-%7C1531726790; loc=620000; Hm_lpvt_a27d3c53126c59f93b8f63a30262cb5e=1531731621'
#     response = requests.post(url=postUrl, data=data,
#                              headers=getHeaders(), verify=False)
#     response.encoding = 'utf-8'
#     parseHtml(html=response.text)

# spiderPost('130000')
# spiderGet('https://www.tvmao.com/program/HEBEI-HEBEI1-w1.html')
# sys.stdout.flush()
# os._exit(0)


# waitSec = 1
# total = 0

# while len(todoUrlSet) > 0:
#     url = todoUrlSet.pop()
#     # try:
#     url = prefix+url
#     # print(url)
#     doneUrlSet.add(url)
#     spiderGet(url)
#     sys.stdout.flush()
#     hrefFile.flush()
#     resFile.flush()
#     # time.sleep(2)
#     # except:
#     #     print('wait ', waitSec, 's, total ', total, 's')
#     #     sys.stdout.flush()
#     #     os._exit(0)
#     #     time.sleep(waitSec)
#     #     todoUrlSet.add(url)


def spiderOneRoot(rootUrl):
    todoUrlSet.clear()
    doneUrlSet.clear()
    # channelsSet.clear()
    todoUrlSet.add(rootUrl)

    failed = 0
    while len(todoUrlSet) > 0:
        postfix = todoUrlSet.pop()
        try:
            doneUrlSet.add(postfix)
            url = prefix+postfix
            spiderGet(url)
            sys.stdout.flush()
            hrefFile.flush()
            resFile.flush()
            failed = 0
        except:
            # print(err)
            todoUrlSet.add(postfix)
            # t = random.randint(0, 30)
            # print('sleep', t, 'sec')
            time.sleep(10)
            failed = failed+1
            print('failed', failed, 'time')
            if failed > 120:
                return

# spiderOneRoot('/program/CCTV')
# os._exit(0)


entryUrl = [
    '/program/CCTV',
    '/program_satellite/AHTV1-w3.html',
    '/program_digital/CCTV3D-w3.html',
    '/program/TVB',
    '/program/AUMEN',
    '/program/STARTV',
    '/program/AUSTRALIANETWORK',
    '/program/HEBEI-HEBEI1-w1.html',
    '/program/XIZANGTV-XIZANGTV1-w1.html',
    '/program/ZJTV-ZJTV1-w1.html',
    '/program/GSTV-GSTV1-w1.html',
    '/program/JXTV-JXTV1-w1.html',
    '/program/LNTV-LNTV1-w1.html',
    '/program/CCQTV-CCQTV1-w1.html',
    '/program/SDTV-SDTV1-w1.html',
    '/program/HAINANTV',
    '/program/YNTV-YNTV1-w1.html',
    '/program/GUIZOUTV-GUIZOUTV1-w1.html',
    '/program/AHTV-AHTV1-w1.html',
    '/program/AHTV-AHTV1-w1.html',
    '/program/JILIN-JILIN1-w1.html',
    '/program/QHTV-QHTV1-w1.html',
    '/program/SCTV-SCTV1-w1.html',
    '/program/NMGTV-NMGTV1-w1.html',
    '/program/HUBEI-HUBEI1-w1.html',
    '/program/NXTV-NXTV2-w1.html',
    '/program/GUANXI-GUANXI2-w1.html',
    '/program/XJTV-XJTV1-w1.html',
    '/program/SHHAI',
    '/program/HLJTV-HLJTV1-w1.html',
    '/program/HNTV-HNTV1-w1.html',
    '/program/HNTV-HNTV1-w1.html',
    '/program/SXTV-SXTV1-w1.html',
    '/program/BTV-BTV1-w1.html',
    '/program/GDTV-GDTV1-w1.html',
    '/program/JSTV-JSTV1-w1.html',
    '/program/TJTV-TJTV1-w1.html',
    '/program/HUNANTV-HUNANTV1-w1.html',
    '/program/SHXITV-SHXITV1-w1.html',
    '/program/FJTV-FJTV2-w1.html'
]

for url in entryUrl:
    spiderOneRoot(url)
