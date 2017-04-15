#_*_ encoding: utf-8 _*_


import re
import requests
import random
import time


class Download:

    def __init__(self):
        self.user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        self.iplist = []
        html = requests.get('http://haoip.cc/tiqu.htm')
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in iplistn:
            i = re.sub('\n', '', ip)
            self.iplist.append(i.strip())

    def get(self, url, timeout, proxy=None, num_retries=6):
        # 浏览器请求头（大部分网站没有这个请求头会报错、请务必加上
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA}

        if proxy == None:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(10)
                    print(
                        'get webpage error, 10s later get the ', num_retries, ' times')
                    return self.get(url, timeout, num_retries - 1)
                else:
                    print('start using proxy...')
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': Ip}
                    return self.get(url, timeout, proxy,)
        else:
            try:
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http': IP}
                return requests.get(url, headers=headers, proxies=proxy)
            except:
                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print(
                        'change the proxy,10s later get the ', num_retries, ' times')
                    print('the proxy now is:', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print('the proxy also no used!')
                    return self.get(url, 3)


down = Download()
