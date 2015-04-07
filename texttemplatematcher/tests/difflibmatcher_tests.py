import unittest
from texttemplatematcher import difflibmatcher
from texttemplatematcher.difflibmatcher import DifflibMatcher, DifflibVars


class DifflibMatcherTest(unittest.TestCase):
    def test_matcher(self):
        text     = "input a string and this will match variables in the template."
        template = "input a {{object}} and this will {{action}}."

        matcher = DifflibMatcher()
        result = matcher.template_match(text, template)
        self.assertEqual(2, len(result), "Should found two result.")

        expected_result_0_var = DifflibVars(v_name="object", start_pos=8, end_pos=14, value="string")
        expected_result_1_var = DifflibVars(v_name="action", start_pos=29, end_pos=60, value="match variables in the template")
        self.assertEqual(expected_result_0_var, result[0])
        self.assertEqual(expected_result_1_var, result[1])

    def test_matcher_result_different_from_fuzzy(self):
        text     = "input a string and this will match variables in the template."
        template = "Enter a {{object}}, and it will {{action}}."

        result = difflibmatcher.template_match(text, template)
        self.assertEqual(1, len(result), "Should found only one result.")

        expected_result_0_var = DifflibVars(v_name="action", start_pos=29, end_pos=60, value="match variables in the template")
        self.assertEqual(expected_result_0_var, result[0])

    def test_matcher_multiple_not_template_in_between(self):
        text = "Hello dude. How are you. This should be good."
        template = "Hello {{first_found}}. zz {{not_be_found}}. This should be {{second_found}}."

        result = difflibmatcher.template_match(text, template)
        self.assertEqual(2, len(result), "Should found only two result.")
        expected_result_0_var = DifflibVars(v_name="first_found", start_pos=6, end_pos=10, value="dude")
        expected_result_1_var = DifflibVars(v_name="second_found", start_pos=40, end_pos=44, value="good")
        self.assertEqual(expected_result_0_var, result[0])
        self.assertEqual(expected_result_1_var, result[1])

    def test_shorthand(self):
        text     = "input a string and this will match variables in the template."
        template = "input a {{object}} and this will {{action}}."

        matcher = DifflibMatcher()
        non_shorthand_result = matcher.template_match(text, template)
        shorthand_result = difflibmatcher.template_match(text, template)
        self.assertEqual(non_shorthand_result, shorthand_result, "Non-shorthand result should equal shorthand result.")

    def test_mark(self):
        text     = "input a string and this will match variables in the template."
        template = "input a {{object}} and this will {{action}}."

        result = difflibmatcher.template_match(text, template)
        expected = "input a {{string}} and this will {{match variables in the template}}."
        marked = difflibmatcher.mark(text, result)
        self.assertEqual(expected, marked)