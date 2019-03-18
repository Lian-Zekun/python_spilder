import requests
from lxml import etree
import csv


def hupu_spilder(url):
    info = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    root = etree.HTML(res.text)
    name = root.xpath('//ul[@class="for-list"]/li//a[@class="truetit"]')
    href = root.xpath('//ul[@class="for-list"]/li//a[@class="truetit"]/@href')
    author = root.xpath('//ul[@class="for-list"]/li//a[@class="aulink"]/text()')
    time = root.xpath('//ul[@class="for-list"]/li//a[@style="color:#808080;cursor: initial; "]/text()')
    for i in range(len(name)):
       if name[i].text:
           info.append([name[i].text, author[i], time[i], 'https://bbs.hupu.com' + href[i]])
       else:
           info.append([name[i][0].text, author[i], time[i], 'https://bbs.hupu.com' + href[i]])
    return info


if __name__ == '__main__':
    fieldnames = ['name', 'author', 'time', 'href']
    f = open('hupu.csv', 'a+', encoding='utf-8')
    f_csv = csv.writer(f)
    f_csv.writerow(fieldnames)
    for i in range(1, 2):
        url = 'https://bbs.hupu.com/lol-{}'.format(i)
        info = hupu_spilder(url)
        f_csv.writerows(info)
    f.close()