Text Template Matcher
=====================

Matchers: Fuzzy Matcher
-----------------------
This matcher is ported from [https://github.com/nathanathan/fuzzyTemplateMatcher](https://github.com/nathanathan/fuzzyTemplateMatcher)

```python
>>> from texttemplatematcher import fuzzymatcher
>>> text     = "input a string and this will match variables in the template."
>>> template = "input a {{object}} and this will {{action}}."
>>> result   = fuzzymatcher.fuzzy_template_match(text, template)
>>> for var in result.vars:
>>>     print("Found '{:}' : '{:}'".format(var.v_name, var.value))
Found 'object' : 'string'
Found 'action' : 'match variables in the template'
>>> print("Marked: {:}".format(fuzzymatcher.mark(text, result.vars)))
Marked: input a {{string}} and this will {{match variables in the template}}.
```

2.
