import unittest
from texttemplatematcher import fuzzymatcher
from texttemplatematcher.fuzzymatcher import FuzzyMatcher, Vars

text = "input a string and this will match variables in the template."
template = "Enter a {{object}}, and it will {{action}}."

class FuzzyMatcherTest(unittest.TestCase):
    def test_matcher(self):
        matcher = FuzzyMatcher()
        result = matcher.fuzzy_template_match(text, template)
        print(result)

        self.assertEqual(2, len(result.vars), "Should found two result.")

        expected_result_0_var = Vars(v_name="object", start=8, end=14, value="string")
        expected_result_1_var = Vars(v_name="action", start=29, end=60, value="match variables in the template")
        self.assertEqual(expected_result_0_var, result.vars[0])
        self.assertEqual(expected_result_1_var, result.vars[1])

    def test_shorthand(self):
        matcher = FuzzyMatcher()
        non_shorthand_result = matcher.fuzzy_template_match(text, template)
        shorthand_result = fuzzymatcher.fuzzy_template_match(text, template)
        self.assertEqual(non_shorthand_result, shorthand_result, "Non-shorthand result should equal shorthand result.")

    def test_mark(self):
        result = fuzzymatcher.fuzzy_template_match(text, template)
        expected = "input a {{string}} and this will {{match variables in the template}}."
        marked = fuzzymatcher.mark(text, result.vars)
        self.assertEqual(expected, marked)