#! coding=utf-8
import os
import logging
import re

from nltk import WordNetLemmatizer, pos_tag, sent_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import csv

"""
对原始语料库进行数据清理
"""


class WordFilter(object):
    """
    词库过滤器
    对语料库进行过滤，只关注词库中的单词之间的关系
    """
    def __init__(self, lex_name=""):
        self.word_list = []
        if not lex_name:
            return

        with open(os.path.join('..', 'lexicon', lex_name), 'r') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                self.word_list.append(row[1].lower())

    def filter(self, word):
        """
        判断检索词是否在词库中
        :param word: 检索词
        :return: bool 是否在词库
        """
        if not self.word_list:  # 词库为空说明不过滤
            return True

        return word in self.word_list


class TextIterator:
    """
    纯文本文件的读取并返回
    """
    def __init__(self, filename, lex_name):
        self.filename = filename
        self.filter = WordFilter(lex_name)

    def __iter__(self):
        filename = os.path.join('..', 'raw', self.filename)
        for line in open(filename, 'r', encoding='utf-8'):
            line = word_tokenize(line)
            line = [lemma(x.lower()) for x in line if self.filter.filter(lemma(x.lower()))]
            if not line:
                continue
            logging.debug(line)
            yield line


def lemma(word):
    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        # elif treebank_tag.startswith('R'):
        #     return wordnet.ADV
        else:
            return wordnet.NOUN

    lemmatizer = WordNetLemmatizer()
    lemma_word = lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos_tag([word])[0][1]))
    return lemma_word


class WikiIterator:
    """
    读取维基百科文件夹并返回
    :param feedback: 迭代器的返回类型
    - word2bow:  返回经过筛选，词形还原，数据清理的词汇数组 ['asdfasdf', 'asdfasdf']
    - sentence:  返回句子和经过筛选和词形还原的句子[('i am a hero.', ['i', 'be', 'hero']), ]
    """
    file_limit = 1  # 读取的文件数限制 3G

    count = 0
    dir_name = 'enwiki'

    def __init__(self, lex_name, feedback='word2bow'):
        self.filter = WordFilter(lex_name)
        self.feedback = feedback  # 该迭代器需要返回的类型

    def __iter__(self):  # 找到enwiki文件夹下的
        dir_name = os.path.join('..', 'raw', self.dir_name)
        for root, dirs, files in os.walk(dir_name):
            if self.count >= self.file_limit:  # 训练文件数量限制，1个文件1M
                break
            for filename in files:
                if self.count >= self.file_limit:  # 训练文件数量限制，1个文件1M
                    break
                file_path = os.path.join(root, filename)
                self.count += 1
                logging.info('at files {}'.format(self.count))
                for line in open(file_path, 'r', encoding='utf-8'):
                    if self.feedback == 'word2bow':
                        line = Cleaner.wiki_cleaner(line)
                        line = [lemma(x) for x in line if self.filter.filter(lemma(x))]
                        if not len(line):
                            continue
                        logging.debug(line)
                        yield line
                    elif self.feedback == 'sentence':
                        sentences = Cleaner.wiki_sen_cleaner(line)
                        for sentence in sentences:
                            lemma_sentence = [lemma(x) for x in sentence if self.filter.filter(lemma(x))]
                            if not len(lemma_sentence):
                                continue
                            yield tuple([sentence, lemma_sentence])
                    else:
                        raise Exception('feedback should be word2bow or sentence')


class Cleaner:
    """
    数据清理
    """

    @staticmethod
    def wiki_cleaner(line):
        def clean_html(raw_html):  # 清除纯HTML中的<标签>
            cleaner = re.compile('<.*?>')
            cleantext = re.sub(cleaner, ' ', raw_html)
            return cleantext

        """
        维基百科文本清理
        """
        sline = line.strip()
        if sline != '':
            rline = clean_html(sline)
            tokenized = word_tokenize(rline)
            sentence = [word.lower() for word in tokenized if word.isalpha()]
            return sentence
        return []

    @staticmethod
    def wiki_sen_cleaner(line):
        def clean_html(raw_html):  # 清除纯HTML中的<标签>
            cleaner = re.compile('<.*?>')
            cleantext = re.sub(cleaner, ' ', raw_html)
            return cleantext
        sline = line.strip()
        if sline != '':
            rline = clean_html(sline)
            sentences = sent_tokenize(rline)
            return sentences
        return []
