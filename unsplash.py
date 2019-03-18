import requests
import time
import random
import threading


urls = []
img_url = []
g_lock = threading.Lock()


def choose_header():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
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
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    ]
    UserAgent = random.choice(user_agent_list)
    return UserAgent


headers = {
        'User-Agent': choose_header(),
        'access-control-allow-origin': 'https://unsplash.com',
        # 'x-per-page': '12'
    }


def set_url():
    """生成页面url"""
    for i in range(1, 11):
        url = 'https://unsplash.com/napi/photos?page={}&per_page=12'.format(i)
        urls.append(url)
    return urls


class GetUrl(threading.Thread):
    """获取每个图片的id和下载路径"""
    def run(self):
        print("{} is running ".format(threading.current_thread))
        while len(urls) > 0:
            g_lock.acquire()
            url = urls.pop()
            g_lock.release()
            req = requests.get(url, headers=headers)
            data = req.json()
            for i in range(12):
                g_lock.acquire()
                img_url.append({'id': data[i]['id'], 'url': data[i]['links']['download']})
                g_lock.release()
            time.sleep(0.5)
        return img_url


class Download(threading.Thread):
    def run(self):
        print("{} is running ".format(threading.current_thread))
        path = 'xxxxxx' #下载路径
        while len(img_url) > 0:
            g_lock.acquire()
            img = img_url.pop()
            g_lock.release()
            res = requests.get(img.get('url'), headers=headers)
            with open(path + "/" + img.get('id') + ".jpg", "wb") as f:
                f.write(res.content)
            time.sleep(0.5)


if __name__ == '__main__':
    start_time = time.time()  # 开始时间
    set_url()
    print(urls)
    get_list = []
    down_list = []
    for i in range(5):
        g = GetUrl()
        g.start()
        get_list.append(g)
    for d in get_list:
        d.join()
    print("链接下载完成")
    for i in range(5):
        g = Download()
        g.start()
        down_list.append(g)
    for d in down_list:
        d.join()
    print("图片下载完成")
    end_time = time.time()  # 结束时间

    print("time:%d" % (end_time - start_time))  # 结束时间-开始时间
