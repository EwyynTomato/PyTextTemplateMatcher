import re
import copy
from base import BaseSimpleRepr
from base import BaseMatcher

class Offset(BaseSimpleRepr):
    """
    Offset object for FuzzyMatcher to represents the position of template variables.
    e.g.
        'That {{rug}} really tied the room together.'
        # offset would be 4, and v_name would be 'rug'
    """
    def __init__(self, offset, v_name):
        self.offset = offset #Starting position of {{variable}}
        self.v_name = v_name #Name of {{variable}}, e.g. {{variable}} is 'variable'

class Memo(BaseSimpleRepr):
    def __init__(self, a, b, val):
        self.a = a
        self.b = b
        self.val = val

class Result(BaseSimpleRepr):
    def __init__(self):
        self.vars = []
        """:type: list[Vars]"""
        self.ld = 0

        self.adjustedld = 0

class Vars(BaseSimpleRepr):
    def __init__(self, v_name, start, end):
        self.v_name = v_name
        self.start = start
        self.end = end

        self.value = None

def _start_var_range(vname, idx, ftm):
    new_ftm = copy.deepcopy(ftm)
    new_ftm.vars = map(lambda v: v, ftm.vars)
    new_ftm.vars.append(Vars(vname, idx, idx))
    return new_ftm


def _set_var_range(vname, idx, ftm):
    class local:
        v_found = False
    def mapvars(v):
        if v.v_name != vname:
            return v
        local.v_found = True
        return Vars(vname, v.start, idx)
    local.v_found = False
    new_ftm = copy.copy(ftm)
    new_ftm.vars = map(mapvars, ftm.vars)
    if not local.v_found:
        new_ftm.vars.append(Vars(vname, idx-1, idx))
    return new_ftm

class FuzzyMatcher(BaseMatcher):
    """
    Directly ported from:
        https://github.com/nathanathan/fuzzyTemplateMatcher

    Docs and readability refactor are welcome
    """
    def __init__(self):
        super(FuzzyMatcher, self).__init__()
        self.offset_map = []
        self.VARIABLE_LD = 0.99
        self._stringystring  = None
        self._templatestring = None
        self._memos = []

    def _replacevariable(self, regex_match):
        """
        Given a regex match object, replace template variable with '*' and add offset info into offset_map
        :param _sre.SRE_Match regex_matches: _sre.SRE_Match object for replacement
        :return: str
        """
        start_pos = regex_match.start()
        v_name = regex_match.groups()[0] #regex: $1
        self.offset_map.append(Offset(start_pos, v_name))
        return "*"

    @staticmethod
    def _find(arr, fun):
        try:
            val = (val for val in arr if fun(val)).next()
        except StopIteration: #Nothing found
            val = None
        return val

    @staticmethod
    def _add_ld(increment, ftm):
        new_ftm = copy.deepcopy(ftm)
        new_ftm.ld = ftm.ld + increment
        return new_ftm

    @staticmethod
    def _reduce_pftms(min_so_far, pftm):
        if not min_so_far:
            return pftm
        if pftm.ld < min_so_far.ld:
            return pftm
        else:
            return min_so_far

    def _memoize(self, fun):
        """:type: list[Memo]"""
        def memoize(a, b):
            memo = self._find(self._memos, lambda memo: (memo.a == a and memo.b == b))
            """:type: Memo"""
            if memo:
                return memo.val
            recursed = fun(a,b)
            self._memos.append(Memo(a, b, recursed))
            value = self._memos[len(self._memos) - 1].val
            return value
        return lambda a, b: memoize(a, b)

    def _ftm_recurse(self, len_a, len_b):
        return self._memoize(lambda a,b: self._recurse(a, b))(len_a, len_b)

    def _recurse(self, len_a, len_b):
        result = Result()
        if len_a == 0:
            result.ld = len_b
            result.vars = map(lambda x: Vars(x.v_name, 0, 0), (offset for offset in self.offset_map if offset.offset < len_b))
            return result
        if len_b == 0:
            result.ld = len_a
            return result

        pftms = []
        v_at_offset = self._find(self.offset_map, lambda x: x.offset == (len_b -1))
        if v_at_offset:
            pftms.append(_set_var_range(v_at_offset.v_name, len_a,
                                             self._add_ld(self.VARIABLE_LD, self._ftm_recurse(len_a - 1, len_b))))
            pftms.append(_start_var_range(v_at_offset.v_name, len_a,
                                               self._ftm_recurse(len_a, len_b - 1)))
        else:
            tempftm = self._ftm_recurse(len_a, len_b - 1)
            pftms.append(self._add_ld(1, tempftm))
            pftms.append(self._add_ld(1, self._ftm_recurse(len_a - 1, len_b)))
            if self._stringystring[len_a - 1] == self._templatestring[len_b - 1]:
                pftms.append(self._ftm_recurse(len_a - 1, len_b - 1))
            else:
                pass
        return reduce(self._reduce_pftms, pftms)

    def fuzzy_template_match(self, text, template):
        """
        :param text:
        :param str template: string representation of template, e.g. "hello {{name}}, I'm {{dude}}."
        :rtype: Result
        """
        self._stringystring = text
        self._templatestring = template

        #- Replace {{variable}} with *, once a time (regex count=1 intead of 0) so .start offset would change
        vreplaced = True
        while vreplaced:
            vreplaced = True
            replaced = re.sub("\{\{(\w*?)\}\}", self._replacevariable, self._templatestring, 1)
            if self._templatestring == replaced:
                vreplaced = False
            else:
                self._templatestring = replaced

        #- Process
        result = self._ftm_recurse(len(self._stringystring), len(self._templatestring))
        variable_text_length = 0
        for var in result.vars:
            var.value = text[var.start:var.end]
            variable_text_length += len(var.value)
        result.adjustedld = int(round(result.ld - (variable_text_length * self.VARIABLE_LD)))

        return result
