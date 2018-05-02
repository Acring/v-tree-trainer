#!coding=utf-8
from gensim import models
import logging
import os
from iterator.iterator import WikiIterator, TextIterator
import csv
"""
训练模型
"""



class CorpusIterator(object):
    """
    语料库迭代器
    打开语料库并逐行返回数据给Word2Vec
    """
    def __init__(self, path):
        """
        :param path: 文件地址
        """
        self.path = path

    def __iter__(self):
        """
        迭代器
        :return: 返回每行的分词
        """
        for line in open(self.path, mode="r", encoding="utf-8"):
            yield line.split(" ")  # 返回一个词语数组


class Trainer(object):
    """
    模型训练器
    """
    min_count = 10  # 最小记数
    size = 200  # 向量维度
    window = 10  # 窗口大小
    model = None

    def __init__(self, corpus_iterator=None, result_name=None, retrain=True):
        """
        :param corpus_iterator: 语料库迭代器
        :param result_name: 训练模型地址
        :param retrain: 是否允许多次训练
        """
        self.corpus_iterator = corpus_iterator
        self.result_name = os.path.join('..', 'model', result_name) if result_name else None
        self.retrain = retrain

    def load_model(self, name=None, bin=False):
        """
        加载模型
        :return:
        """
        if name:
            self.result_name = os.path.join('..', 'model', name)

        try:
            self.model = models.KeyedVectors.load_word2vec_format(self.result_name, binary=True) \
                if bin else models.Word2Vec.load(self.result_name)
        except Exception as e:
            logging.error("加载模型失败:{}".format(e))
            return

    def train_model(self):
        """
        训练模型
        :return:
        """

        if not os.path.exists(self.result_name):  # 模型已存在
            model = models.Word2Vec(self.corpus_iterator, min_count=self.min_count, size=self.size, window=self.window)
        elif self.retrain:
            logging.info("模型已存在, 再次训练")
            model = models.Word2Vec.load(self.result_name)
        else:
            logging.error("模型存在,禁止再次训练")
            return

        model.train(self.corpus_iterator, total_examples=model.corpus_count, epochs=model.iter)
        model.save(self.result_name)

        self.model = model

    def test_model(self, function):
        """
        测试模型
        :param function 测试函数(model)传入训练模型
        :return:
        """
        print(self.model)
        if not self.model:
            logging.error("模型未加载或未训练")
            return
        if not hasattr(function, "__call__"):
            logging.error("未传入测试函数")
        function(self.model)


def train_wiki():
    wiki_iterator = WikiIterator('COCA20000.csv')
    manager = Trainer(wiki_iterator, 'enwiki')
    manager.train_model()


def train_test():
    iterator = TextIterator('wiki_chinese_preprocessed.simplied.txt', 'COCA20000.csv')
    manager = Trainer(iterator, 'test')
    manager.train_model()


def train_sub():
    """
    通过电影字幕进行相似词训练
    :return:
    """
    iterator = TextIterator('sub_1.txt', 'COCA20000.csv')
    manager = Trainer(iterator, 'sub')
    manager.train_model()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    train_sub()
