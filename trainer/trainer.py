from bs4 import BeautifulSoup
from app.parser.basemisc import BaseParser

class RegexTrainer(object):
    def load(self, filename):
        """
        Loads
        :type filename: str
        :param filename:
        :return:
        """
        with open(filename, "r") as f:
            traindata = f.read()

    def loads(self, string):
        pass
        # s = string.split("\n")
        # text = s[5]
        # print(text)
        # print(nltk.pos_tag(nltk.word_tokenize(text)))




if __name__ == '__main__':
    pass

# p = RegexTrainer()
# soup = p.load("data/textplain.txt")