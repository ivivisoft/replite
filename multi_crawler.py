import os
import time
import threading
import multiprocessing
from MogoQueue import MogoQueue
from Download import down
from bs4 import BeautifulSoup
from pymongo import MongoClient

SLEEP_TIME = 1


def mzitu_crawler(max_threads=10):
    crawl_queue = MogoQueue('reptile', 'crawl_queue')
    client = MongoClient()
    db = client['reptile']
    mzitu_collection = db['mzitumany']

    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print('the queue is empty!')
                break
            else:
                title = crawl_queue.pop_title(url)
                mkdir(title)
                html(url)
                if mzitu_collection.find_one({'主题页面': url}):
                    print('The title already repliled')
                else:
                    html(url)
                    post = {
                        '标题': title,
                        '主题页面': url,
                        '获取时间': datetime.datetime.now()
                    }
                    mzitu_collection.save(post)

    def html(href):
        img_a_girl_html = down.get(href, 3)
        img_a_girl = BeautifulSoup(img_a_girl_html.text, 'lxml')
        max_span = img_a_girl.find(
            'div', class_='pagenavi').find_all('span')[-2].get_text()
        img(href)
        for page in range(2, int(max_span) + 1):
            page_url = href + '/' + str(page)
            img(page_url)

    def img(url):
        girl = down.get(url, 3)
        img_soup = BeautifulSoup(girl.text, 'lxml')
        img_url = img_soup.find(
            'div', class_='main-image').find('img')['src']
        name = img_url[-9:-4]
        save(img_url, name)

    def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(
            os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu1', path))
        if not isExists:
            print('create a dir: ' + path)
            os.makedirs(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu1', path))
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu1', path))
            return True
        else:
            print('the dir:' + path + ' is alreay exist')
            os.chdir(
                os.path.join('/Users/andysoft/pythonwebdriver/reptile/mzitu1', path))
            return False

    def save(img_url, name):
        img = down.get(img_url, 3)
        print('save a image who name is:' + name + '.jpg')
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            thread = threading.Thread(target=pageurl_crawler)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('start process nums:', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
