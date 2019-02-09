import requests
import platform
import os
import time
from urllib import request
from lxml import etree
from selenium import webdriver


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/'
    }


def get_url(url):
    """从歌单中获取歌曲链接"""

    req = requests.get(url, headers=headers)

    root = etree.HTML(req.text)
    items = root.xpath('//ul[@class="f-hide"]//a')

    return items


def download_song(song_id, song_name):
    """从链接中提取id和名字，通过外链下载歌曲"""

    url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)

    req = requests.get(url, headers=headers, allow_redirects=False)
    song_url = req.headers['Location']
    try:
        request.urlretrieve(song_url, path + "/" + song_name + ".mp3")
        print("{}--下载完成".format(song_name))
    except:
        print("{}--下载失败".format(song_name))


def download(items):
    """全部歌曲下载"""

    for item in items:
        song_id = item.get('href').strip('/song?id=')
        song_name = item.text
        download_song(song_id, song_name)
    print("－－－－－－－下载完成－－－－－－－")


# 根据歌手下载
def artist_id_down(id):
    """根据歌手id或歌单id下载全部歌曲"""

    artist_url = 'https://music.163.com/artist?id={}'.format(id)

    items = get_url(artist_url)
    download(items)


# 根据歌单下载
def playlist_id_down(id):
    playlist_url = 'https://music.163.com/playlist?id={}'.format(id)

    items = get_url(playlist_url)
    download(items)


def get_song_name(url):
    """在歌曲页面获得名字"""

    req = requests.get(url, headers=headers)

    root = etree.HTML(req.text)
    name = root.xpath('//em[@class="f-ff2"]/text()')

    return name[0]


# 根据歌曲下载
def song_id_down(id):
    """根据歌曲id下载"""

    url = 'https://music.163.com/song?id={}'.format(id)

    name = get_song_name(url)
    download_song(id, name)


def selenium_get_html(url):
    """通过selenium获得页面源码"""

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(
            'User-Agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"')
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        driver.switch_to.frame('contentFrame')
        return driver.page_source
    except:
        pass


def search_input_song(url):
    """获取歌曲名字和id"""

    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="srchsongst"]//div[@class="td w0"]//div[@class="text"]/a[1]/@href')
    name = root.xpath('//div[@class="srchsongst"]//div[@class="td w1"]//div[@class="text"]/a[1]/text()')

    if not id:
        return "请输入正确的歌曲名称"
    id = [i.strip('/song?id==') for i in id]
    return zip(name, id)


def search_input_artist(url):
    """获取歌手id"""

    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="u-cover u-cover-5"]/a[1]/@href')

    if not id:
        return "请输入正确的歌手名称"
    return id[0].strip('/artist?id==')


def search_input_playlist(url):
    """获取歌单名字和id"""

    html = selenium_get_html(url)

    root = etree.HTML(html)
    id = root.xpath('//div[@class="u-cover u-cover-3"]/a/@href')
    name = root.xpath('//div[@class="u-cover u-cover-3"]//span/@title')

    if not id:
        return "请输入正确的歌单名称"
    id = [i.strip('/playlist?id==') for i in id]
    return zip(name, id)


def main(name, choose_id):
    if choose_id == 1:
        url = 'https://music.163.com/#/search/m/?s={}&type=1'.format(name)
        com = search_input_song(url)
        ids = []
        for i, j in com:
            ids.append(j)
            print("演唱者:{0}-------id:{1}".format(i, j))
        while True:
            id = input("请输入需要下载的id(输入q退出):")
            if id == 'q':
                return
            if id in ids:
                song_id_down(id)
                return
            print("请输入正确的id!!!")
    elif choose_id == 2:
        url = 'https://music.163.com/#/search/m/?s={}&type=100'.format(name)
        id = search_input_artist(url)
        artist_id_down(id)
    elif choose_id == 3:
        url = 'https://music.163.com/#/search/m/?s={}&type=1000'.format(name)
        com = search_input_playlist(url)
        ids = []
        for i, j in com:
            ids.append(j)
            print("歌单名称:{0}-------id:{1}".format(i, j))
        while True:
            id = input("请输入需要下载的id(输入q退出):")
            if id == 'q':
                return
            if id in ids:
                playlist_id_down(id)
                return
            print("请输入正确的id(输入q退出):")


def recognition():
    """判断系统,执行清屏命令"""
    sysstr = platform.system()
    if (sysstr == "Windows"):
        os.system('cls')
    elif (sysstr == "Linux"):
        os.system('clear')


if __name__ == '__main__':
    path = input("请输入完整路径地址:")
    if not os.path.exists(path):
        os.makedirs(path)
    while True:
        print("=========================")
        print("请按提示选择搜索类型:")
        print("1.歌曲")
        print("2.歌手")
        print("3.歌单")
        print("4.退出")
        print("=========================")
        choose_id = int(input("搜索类型:"))
        if choose_id == 4:
            break
        elif choose_id != 1 and choose_id != 2 and choose_id != 3:
            print("请按要求输入!!!")
            continue
        else:
            recognition()
            name = input("请输入搜索内容:")
            main(name, choose_id)
            print("3秒后返回主页面")
            time.sleep(3)
