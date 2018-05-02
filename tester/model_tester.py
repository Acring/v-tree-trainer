import csv
import os
from trainer.model_trainer import Trainer


def test_sub():
    def test1(model):
        while True:
            word = input()
            try:
                print(model.wv.most_similar(word, topn=20))
            except Exception as e:
                print('没有这个词啊: {}'.format(e))
    manager = Trainer()
    manager.load_model('sub', bin=False)
    manager.test_model(test1)


def test_wiki():
    def test1(model):
        while True:
            word = input()
            try:
                print(model.wv.most_similar(word, topn=20))
            except Exception as e:
                print('没有这个词啊: {}'.format(e))
    manager = Trainer()
    manager.load_model('enwiki', bin=False)
    manager.test_model(test1)


def test_by_lexicon(lex_name, model_name):
    """
    根据词库自动测试模型的好坏
    :param lex_name:
    :param model_name:
    :return:
    """
    with open(os.path.join('..', 'lexicon', lex_name)) as f:
        manager = Trainer()
        manager.load_model(model_name)
        model = manager.model

        f_csv = csv.reader(f)
        for row in f_csv:
            word = row[1]
            try:
                print('word: {}, similar:{}'.format(word, model.wv.most_similar(word, topn=10)))
            except Exception as e:
                print('word: {}, {}'.format(word, e))

if __name__ == '__main__':
    test_sub()