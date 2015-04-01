import pycrfsuite
import pickle
import nltk

# class TrainingUtils(object):
#     def load(self, filename):
#         with open(filename, "r") as f:
#             traindata = f.read()
#         self.loads(traindata)
#
#     def loads(self, string):
#         s = string.split("\n")
#         text = s[5]
#         print(text)
#         print(nltk.pos_tag(nltk.word_tokenize(text)))

# if __name__ == '__main__':
#     pass
#     # trainingutils = TrainingUtils()
#     # trainingutils.load("data/textplain.txt")

# txt = "input a string and this will match variables in the template."
# templt = "Enter a {{object}}, and it will {{action}}."
#
# fuzzy_matcher = FuzzyMatcher()
# result = fuzzy_matcher.fuzzy_template_match(txt, templt)
# print(result)