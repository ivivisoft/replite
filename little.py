#_*_ encoding: utf-8 _*_


from bs4 import BeautifulSoup
import os
from Download import down
from pymongo import MongoClient
import datetime


class Mzitu:

    def __init__(self):
        client = MongoClient()
        db = client['reptile']
        self.mzitu_collection = db['mzitu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def all_url(self, url):
        html = down.get(url, 3)
        Soup = BeautifulSoup(html.text, 'lxml')
        imgs_list = Soup.find('ul', id='pins').select('span > a')
        for imgs in imgs_list:
            title = imgs.get_text()
            self.title = title
            self.mkdir(title)
            href = imgs['href']
            self.url = href
            if self.mzitu_collection.find_one({'主题页面': href}):
                print('The title already repliled')
            else:
                self.html(href)
                post = {
                    '标题': self.title,
                    '主题页面': self.url,
                    '图片地址': self.img_urls,
                    '获取时间': datetime.datetime.now()
                }
                self.mzitu_collection.save(post)
                self.title = ''
                self.url = ''
                self.img_urls = []

    def html(self, href):
        img_a_girl_html = down.get(href, 3)
        img_a_girl = BeautifulSoup(img_a_girl_html.text, 'lxml')
        max_span = img_a_girl.find(
            'div', class_='pagenavi').find_all('span')[-2].get_text()
        self.img(href)
        for page in range(2, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, url):
        girl = down.get(url, 3)
        img_soup = BeautifulSoup(girl.text, 'lxml')
        img_url = img_soup.find(
            'div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        name = img_url[-9:-4]
        self.save(img_url, name)

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(
            os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu', path))
        if not isExists:
            print('create a dir: ' + path)
            os.makedirs(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu', path))
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu', path))
            return True
        else:
            print('the dir:' + path + ' is alreay exist')
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu', path))
            return False

    def save(self, img_url, name):
        img = down.get(img_url, 3)
        print('save a image who name is:' + name + '.jpg')
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()


mzitu = Mzitu()
mzitu.all_url('http://www.mzitu.com')
