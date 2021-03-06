# -*- coding: utf-8 -*-
import logging

import re
from base import BaseMatcher, BaseSimpleRepr
from difflib import SequenceMatcher

class DifflibVars(BaseSimpleRepr):
    def __init__(self, v_name, start_pos=0, end_pos=0, value=""):
        self.v_name    = v_name     # template_variable_names
        self.value     = value      # matched_text
        self.start_pos = start_pos  # starting index of matched_text
        self.end_pos   = end_pos    # end index of matched_text

    def __eq__(self, other):
        is_equal = isinstance(other, self.__class__)
        if is_equal:
            is_equal = is_equal and (self.v_name == other.v_name)
            is_equal = is_equal and (self.value == other.value)
            is_equal = is_equal and (self.start_pos == other.start_pos)
            is_equal = is_equal and (self.end_pos == other.end_pos)
        return is_equal

class DifflibMatcher(BaseMatcher):
    """
    Simple template matcher using difflib sequence mathcer
    """
    def __init__(self):
        super(DifflibMatcher, self).__init__()
        self._templatestring = None
        """:type: str"""
        self._variablenames  = [] # List to store Vars (containing template_variable_names, matched_text).
                                  # The reason for using list is to preserve order.
        """:type: list[Vars]"""
        self._v_found        = 0  # current number of template variable being processed

    def _replacevariable(self, regex_match):
        """
        Given a regex match object, replace template variable with u"\U0000FFFF" and store the variable name
        :param _sre.SRE_Match regex_match: _sre.SRE_Match object for replacement
        :return: str
        """
        v_name = regex_match.groups()[0] #regex: $1
        self._variablenames.append(DifflibVars(v_name))
        return u"\U0000FFFF"

    def _mark_template_variable(self):
        """
        Replace {{variable}} with u"\U0000FFFF".
        In contrast to fuzzymatcher, we don't really care about the offset here
        """
        self._templatestring = re.sub("\{\{(.*?)\}\}", self._replacevariable, self._templatestring)

    def _find_replaced_sequences(self, text, template, offset=0, depth=0, max_recursive_depth=3):
        """
        Find replaced sequences and return them as list of result

        The basic idea is as the following:
            >>> #\U0000FFFF is the character put in replacement of template variable string (see self._mark_template_variable)
            >>> template = "private \U0000FFFF currentThread;"
            >>> text     = "abc private volatile abc currentThread; def"
            >>>
            >>> seqmatcher = SequenceMatcher(lambda x: x == " ", template, text)
            >>> for i in seqmatcher.get_opcodes():
            >>>     print("{: <30}: {:} ~ {:}".format(str(i), template[i[1]:i[2]], text[i[3]:i[4]]))
            ('insert', 0, 0, 0, 4)        :  ~ abc
            ('equal', 0, 8, 4, 12)        : private  ~ private
            ('replace', 8, 18, 12, 24)    : \U0000FFFF ~ volatile abc
            ('equal', 18, 33, 24, 39)     :  currentThread; ~  currentThread;
            ('insert', 33, 33, 39, 79)    :  ~  private volatile abc currentThread; def
        Using difflib's SequenceMatcher, we define texts that are in state of 'replace' replacing single u'\U0000FFFF' as the matching string.

        Added:
            If one or more \U0000FFFF is within a text are being replaced,
            recursively check the replaced template and ends the recursion if
            max depth is reached or input sequence and output sequence is equal.

        :rtype: list[Vars]
        """
        seqmatcher = SequenceMatcher(lambda x: x == " ", template, text)
        logging.debug("DifflibSequenceMatcher: check opscode")
        for opscode in seqmatcher.get_opcodes():
            template_text      = template[opscode[1]:opscode[2]]
            replaced_with_text = text[opscode[3]:opscode[4]]

            logging.debug("[{:}] {:}, {:} ~ {:}".format(depth, str(opscode), repr(template_text), repr(replaced_with_text)))
            state = opscode[0]
            if state == "replace":
                if template_text == u"\U0000FFFF":
                    self._variablenames[self._v_found].value     = replaced_with_text
                    self._variablenames[self._v_found].start_pos = offset + opscode[3]
                    self._variablenames[self._v_found].end_pos   = offset + opscode[4]
                    logging.debug("[{:}] Found: ({:}, {:}, {:}, offset={:})".format(depth, replaced_with_text, opscode[3], opscode[4], offset))
                    self._v_found += 1
                elif u"\U0000FFFF" in template_text:
                    # Not entirely "\U0000FFFF", meaning that the matched template variable may be empty, but let's check deeper
                    if (depth == max_recursive_depth) or (template_text == template):
                        # Max recursive depth has been reached, or the recursive call result is the same with the input parameter
                        self._v_found += template_text.count(u"\U0000FFFF") #May have multiple occurences of \u0000ffff that are replaced
                    else:
                        self._find_replaced_sequences(replaced_with_text, template_text, offset+opscode[3], depth+1)

        #Filter out non-matched strings
        result = list(var for var in self._variablenames if var.end_pos != 0)

        return result

    def template_match(self, text, template):
        """
        :param text: input text to be tested against
        :param str template: string representation of template, e.g. "hello {{name}}, I'm {{dude}}."
        :rtype: list[DifflibVars]
        """
        self._templatestring = template
        self._mark_template_variable()
        self._v_found = 0
        result = self._find_replaced_sequences(text, self._templatestring)
        logging.debug("Difflib result: " + repr(result))
        return result

def mark(text, ivars, prefix="{{", suffix="}}"):
    """
    Mark text with matched result
    e.g.
        >>> from texttemplatematcher import difflibmatcher
        >>> text     = "input a string and this will match variables in the template."
        >>> template = "input a {{object}} and this will {{action}}."
        >>> result   = difflibmatcher.template_match(text, template)
        >>> difflibmatcher.mark(text, result.vars)
        'input a {{string}} and this will {{match variables in the template}}.'

    :param str text: text to be marked
    :param list[DifflibVars] ivars: result returned from template_match function
    :param str prefix: marking prefix, e.g. 'string' + 'prefix:{{' => '{{string'
    :param str suffix: marking suffix, e.g. 'string' + 'suffix:}}' => 'string}}'
    :rtype: str
    """
    marked = text
    for var in ivars[::-1]: #Replace backwards so position offset won't mess with our result
        replaced = "{:}{:}{:}".format(prefix, marked[var.start_pos:var.end_pos], suffix)
        marked = marked[:var.start_pos] + replaced + marked[var.start_pos + len(replaced) - (len(prefix) + len(suffix)):]
    return marked

def template_match(text, template):
    """
    Shorthand function call to: DifflibMatcher().template_match(text, template)
    :param text: input text to be tested against
    :param str template: string representation of template, e.g. "hello {{name}}, I'm {{dude}}."
    :rtype: list[DifflibVars]
    """
    return DifflibMatcher().template_match(text, template)
