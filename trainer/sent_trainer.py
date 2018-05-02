import nltk


"""
例句训练器
"""


class SentTrainer:
    """
    例句训练需要根据一个词库lex和一个句子迭代器和一个word2vec模型来工作
    根据词库来确定这个句子中包含了需要的单词
    句子迭代器返回一行一行句子
    word2vec模型用来确定该句子的良好度
    """



