import unittest
from texttemplatematcher import fuzzymatcher
from texttemplatematcher.fuzzymatcher import FuzzyMatcher, FuzzyVars

text = "input a string and this will match variables in the template."
template = "Enter a {{object}}, and it will {{action}}."

class FuzzyMatcherTest(unittest.TestCase):
    def test_matcher(self):
        matcher = FuzzyMatcher()
        result = matcher.template_match(text, template)
        self.assertEqual(2, len(result.vars), "Should found two result.")

        expected_result_0_var = FuzzyVars(v_name="object", start=8, end=14, value="string")
        expected_result_1_var = FuzzyVars(v_name="action", start=29, end=60, value="match variables in the template")
        self.assertEqual(expected_result_0_var, result.vars[0])
        self.assertEqual(expected_result_1_var, result.vars[1])

    def test_shorthand(self):
        matcher = FuzzyMatcher()
        non_shorthand_result = matcher.template_match(text, template)
        shorthand_result = fuzzymatcher.template_match(text, template)
        self.assertEqual(non_shorthand_result, shorthand_result, "Non-shorthand result should equal shorthand result.")

    def test_mark_default(self):
        result = fuzzymatcher.template_match(text, template)
        expected = "input a {{string}} and this will {{match variables in the template}}."
        marked = fuzzymatcher.mark(text, result.vars)
        self.assertEqual(expected, marked)

    def test_mark_custom_prefix_suffix(self):
        result = fuzzymatcher.template_match(text, template)
        expected = 'input a <span class="span">string</span> and this will <span class="span">match variables in the template</span>.'
        marked = fuzzymatcher.mark(text, result.vars, prefix='<span class="span">', suffix='</span>')
        self.assertEqual(expected, marked)