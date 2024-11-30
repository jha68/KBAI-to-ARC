
def is_var(x):
    """
    A helper function that checks if the provided expression x is a variable,
    i.e., a string that starts with ?.

    >>> is_variable('?x')
    True
    >>> is_variable('x')
    False
    """
    return isinstance(x, str) and len(x) > 0 and x[0] == "?"

def substitute(s: dict, x: tuple):
    """
    A helper function that substitute the bindings from s into the expression x.

    >>> substitute({'?x': 'Chris', '?y': 'Dog'}, ('likes', '?x', '?y'))
    ('likes', 'Chris', 'Dog')

    >>> substitute({'?x': 'Dog', '?y': ('owner', '?x')}, ('likes', '?y', '?x'))
    ('likes', ('owner', 'Dog'), 'Dog')

    >>> substitute({'?x': 'Dog'}, '?x')
    'Dog'
    """
    if x in s:
        return substitute(s, s[x])
    elif isinstance(x, tuple):
        return tuple(substitute(s, xi) for xi in x)
    else:
        return x

def unify(x, y, s=()):
    """
    Unify expressions x and y given a provided substitution s.  By default s is
    (), which gets recognized and replaced with an empty dictionary.  Return a
    substitution (a dict) that will make x and y equal or, if this is not
    possible, then it returns None.

    >>> unify(('likes', '?a', 'B'), ('likes', 'A', 'B'), {})
    {'?a': 'A'}

    >>> unify(('likes', '?a', 'B'), ('likes', 'A', '?b'), {})
    {'?a': 'A', '?b': 'B'}
    """
    if s == ():
        s = {}

    ####### IMPLEMENT THIS FUNCTION #########
    if x == y:
        return s
    elif is_var(x):
        return unify_var(x, y, s)
    elif is_var(y):
        return unify_var(y, x, s)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for xi, yi, in zip(x, y):
            s = unify(xi, yi, s)
            if s is None:
                return None
        return s
    else:
        return None
def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    else:
        s[var] = x
        return s

def pattern_match(query, kb, substitution=None):
    """
    Similar to unify, but operates over multiple predictes. A query is a list
    of predicates, some of which may contain variables. A knowledge base (kb) is
    a list of predicates without any variables. Substitutions is a dictionary
    mapping variable to values.

    >>> pattern_match([('likes', '?x', 'Dog'), ('has', '?x', 'food')], [('likes', 'Chris', 'Dog'), ('likes', 'Fred', 'Dog'), ('likes', 'Elizabeth', 'Dog'), ('has', 'Chris', 'food'), ('has', 'Elizabeth', 'food')])
    [{'?x': 'Chris'}, {'?x': 'Elizabeth'}]
    """
    if substitution is None:
        substitution = {}

    ####### IMPLEMENT THIS FUNCTION #########
    results = []
    for k in kb:
        new_subs = unify(query[0], k, substitution.copy())
        if new_subs is not None:
            if len(query) == 1:
                results.append(new_subs)
            else:
                more_results = pattern_match(query[1:], kb, new_subs)
                results.extend(more_results)
    return results
