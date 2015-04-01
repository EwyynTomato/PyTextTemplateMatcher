from methods.trainer import FuzzyMatcher

txt = "input a string and this will match variables in the template."
templt = "Enter a {{object}}, and it will {{action}}."

fuzzy_matcher = FuzzyMatcher()
result = fuzzy_matcher.fuzzy_template_match(txt, templt)
print(result)