#!coding=utf-8
import os
import random
import requests
import re
import csv
import time
"""
翻译训练器
根据相应的词库去Vocabulary抓取相应的翻译

英英互译: Vocabulary
"""

VOC_URL = 'https://www.vocabulary.com/dictionary/{}'  # vocabulary词典地址

headers = {
    'authority': 'www.vocabulary.com',
    'method': 'GET',
    'path': '/dictionary/inherit',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'tz=Asia/Shanghai; guid=20337ab5ab4c61952abc5afec792f2b4; autologin=1; AWSALB=+n8V1qUtsEbZnoDDkHHDp5rVgOch7Bd2SQoiAuYt7IDyCSv2s+cs1dWaa65q1cI1J+eAPF12++HZbd27lBGm2VcWls4lr+lKZ4/zY0oidiW4UCF5plAjfgZg+/aa; _asid=000PPIDn5; JSESSIONID=0BD06854B025A6E76F0A0F9FD301CF96',
    'referer': 'https://www.vocabulary.com/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():

    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


class TransTrainer:

    def __init__(self, lex_name):
        self.lex_name = lex_name  # lexicon 词库地址

    def run(self):
        trans_headers = ['word', 'short', 'long']
        trans_rows = []
        with open(os.path.join('..', 'lexicon', self.lex_name), mode='r') as f:

            f_csv = csv.reader(f)
            for row in f_csv:
                time.sleep(random.randint(1, 3))  # 间隔时间，防封IP
                word = row[1]
                proxies = {'http': 'http://{}'.format(get_proxy())}
                print(proxies)
                r = requests.get(VOC_URL.format(word), headers=headers, proxies=proxies)
                html = r.text
                short = self._get_short(html=html, word=word)
                short = ''if not short else short
                long = self._get_long(html=html, word=word)
                long = '' if not long else long
                print((word, short, long))
                trans_rows.append((word, short, long))

        with open(os.path.join('..', 'lexicon', 'trans_'+self.lex_name), 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(trans_headers)
            f_csv.writerows(trans_rows)

    @staticmethod
    def _get_short(html, word):
        """
        获取词的简介
        :param html: 爬取下的HTML
        :param word: 搜索的词，用于替换
        :return: string 词的简介
        """
        p = re.findall('<p class="short">(.*?)</p>', html)
        if not len(p):
            return None

        clean_i = re.compile(r'(<i>.*?</i>)')
        short = re.sub(clean_i, word, p[0])

        return short

    @staticmethod
    def _get_long(html, word):
        """
        获取词的长介绍
        :param html: 爬取下的HTML
        :param word: 搜索的词，用于替换
        :return: string 词的长介绍
        """
        p = re.findall('<p class="long">(.*?)</p>', html)
        if not len(p):
            return None

        clean_i = re.compile(r'(<i>.*?</i>)')
        long = re.sub(clean_i, word, p[0])

        return long


if __name__ == '__main__':
    trans_trainer = TransTrainer('COCA20000.csv')
    trans_trainer.run()
