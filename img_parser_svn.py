import os.path
import re

import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "*/*",
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/94.0.4606.85 YaBrowser/21.11.3.940 Yowser/2.5 Safari/537.36 "
}


class ImgParserSVN:
    k = 0

    def get_item_href(self, article):
        self.k += 1
        url = f'https://svn-video.ru/search?search_query={article}'
        r1 = requests.get(url, headers=headers)

        search_result = BeautifulSoup(r1.text, 'lxml')
        product_items = search_result.find_all(class_='product_item hit '
                                                      'w_xs_full '
                                                      'isotope-item')
        if product_items:
            for item in product_items:
                if re.search(r'\b{}\b'.format(article),
                             item.find(class_='m_bottom_10').text):
                    self.item_href = item.find('a')['href']
                    break
        else:
            print(f'Внимание! Камера {self.k, article} не найдена на сайте')
            self.item_href = None

    def get_img_url(self, article):
        self.get_item_href(article)
        try:
            r2 = requests.get(self.item_href, headers=headers)
            search_item = BeautifulSoup(r2.text, 'lxml')
            img_url = search_item.find(id='zoom_image')['src']
            self.img_url = 'http://svn-video.ru' + img_url
            return self.img_url
        except Exception:
            self.img_url = None

    def save_img(self, article):
        response = requests.get(self.img_url, headers=headers)
        if response.status_code == 200:
            disk_dir = r"C:\Users\Igor\Desktop\Photos_2"
            with open(os.path.join(disk_dir, '{}. {}.png'.
                    format(self.k, article)), 'wb') as f:
                f.write(response.content)
        else:
            print('Не удалось получить доступ к сайту для скачания картинки')
