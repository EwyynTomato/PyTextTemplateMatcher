from matcher import fuzzymatcher

txt = "input a string and this will match variables in the template."
templt = "Enter a {{object}}, and it will {{action}}."

result = fuzzymatcher.fuzzy_template_match(txt, templt)
print(result.vars)
for var in result.vars:
    print(var.v_name)

# def train(self, text=None):
#     super(FuzzyMatcher, self).train()

# p = RegexTrainer()
# soup = p.load("data/textplain.txt")

# s = string.split("\n")
# text = s[5]
# print(text)
# print(nltk.pos_tag(nltk.word_tokenize(text)))
