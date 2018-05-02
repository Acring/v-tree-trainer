#! coding=utf-8


"""
词典训练器
"""
import os

import logging
from gensim import corpora
from iterator.iterator import WikiIterator, TextIterator


class DicTrainer:

    def __init__(self, iterator):
        self.iterator = iterator

    def wiki_trainer(self):
        dic = corpora.Dictionary()
        documents = []
        count = 0
        for line in self.iterator:
            logging.debug(line)
            documents.append(line)
            if len(documents) == 10:
                count += 1
                logging.info('at documents #{}'.format(count * 10))
                dic.add_documents(documents)
                documents = []
        dic.save(os.path.join('..', 'dictionary', 'enwiki'))

    def test_trainer(self):
        dic = corpora.Dictionary()
        documents = []
        count = 0
        for line in self.iterator:
            documents.append(line)
            if len(documents) == 100:
                count += 1
                print('document #{}'.format(count * 10))
                new_dic = corpora.Dictionary(documents)
                dic.merge_with(new_dic)
                documents = []

        dic.save(os.path.join('..', 'dictionary', 'test'))

    def subtitle_trainer(self):
        dic = corpora.Dictionary()
        documents = []
        count = 0
        for line in self.iterator:
            documents.append(line)
            if len(documents) == 100:
                count += 1
                print('document #{}'.format(count * 100))
                dic.add_documents(documents=documents)
                documents = []
        dic.save(os.path.join('..', 'dictionary', 'sub'))


def train_test():
    iterator = TextIterator('wiki_chinese_preprocessed.simplied.txt', 'COCA20000.csv')
    trainer = DicTrainer(iterator)
    trainer.test_trainer()


def train_wiki():
    iterator = WikiIterator(lex_name='COCA20000.csv')
    trainer = DicTrainer(iterator)
    trainer.wiki_trainer()


def train_sub():
    iterator = TextIterator('sub_1.txt', 'COCA20000.csv')
    trainer = DicTrainer(iterator)
    trainer.subtitle_trainer()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    train_sub()