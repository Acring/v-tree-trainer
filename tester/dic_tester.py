import csv
import os

from gensim import corpora
from pyecharts import Line


def test_dic(dic_name):
    dic = corpora.Dictionary().load(os.path.join('..', 'dictionary', dic_name))

    print(len(dic))
    # 按词出现文档的次个数对词进行排序
    while True:

        word = input()
        try:
            # 获取某个词的id
            id = dic.token2id[word]
            print('id:{}'.format(id))

            # 用id获取某个词
            print(dic[id])

            # 用id获取几个文档中出现过这个词
            print(dic.dfs[id])
            print(dic.dfs[id]/dic.num_docs)
        except KeyError as e:
            print('不存在单词: {}'.format(e))


def test_by_lexicon(lex_name, dic_name):
    with open(os.path.join('..', 'lexicon', lex_name)) as f:
        dic = corpora.Dictionary.load(os.path.join('..', 'dictionary', dic_name))
        f_csv = csv.reader(f)

        for row in f_csv:
            word = row[1]
            try:
                wid = dic.token2id[word]
                print('id:{}, word:{}, dfs:{}, freq:{}'.format(wid, word, dic.dfs[wid], dic.dfs[wid]/dic.num_docs))
            except KeyError as e:
                print('word: {} 未被统计到'.format(word))

        # for x in dic:
        #     print(dic[x])


def chart_by_lexicon(lex_name, dic_name, title):
    with open(os.path.join('..', 'lexicon', lex_name)) as f:
        dic = corpora.Dictionary.load(os.path.join('..', 'dictionary', dic_name))
        f_csv = csv.reader(f)
        sorted_dic = sorted(dic.dfs.items(), key=lambda x: x[1], reverse=True)
        line = Line(title)
        line.add("词频分布", [dic[word[0]] for word in sorted_dic], [word[1]/dic.num_docs for word in sorted_dic], is_smooth=True)
        line.render(os.path.join('..', 'charts', title+'.html'))
        print('[√]生成完毕')

if __name__ == '__main__':
    # test_dic('sub')
    chart_by_lexicon('COCA20000.csv', 'sub', 'Subtitle')
