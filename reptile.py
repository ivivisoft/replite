from Download import down
from MogoQueue import MogoQueue
from bs4 import BeautifulSoup

spider_queue = MogoQueue('reptile', 'crawl_queue')


def start(url):
    respone = down.get(url, 3)
    Soup = BeautifulSoup(respone.text, 'lxml')
    imgs_list = Soup.find('ul', id='pins').select('span > a')
    for imgs in imgs_list:
        title = imgs.get_text()
        href = imgs['href']
        spider_queue.push(href, title)


if __name__ == '__main__':
    start('http://www.mzitu.com')
