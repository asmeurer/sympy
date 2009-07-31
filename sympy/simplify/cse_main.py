""" Tools for doing common subexpression elimination.
"""

from sympy import Symbol, Basic, var, C, S, Function
from sympy.core import sympify, Rational
from sympy.core.numbers import ilcm
from sympy.polys import factor
from sympy.utilities.iterables import postorder_traversal

import cse_opts

# (preprocessor, postprocessor) pairs which are commonly useful. They should
# each take a sympy expression and return a possibly transformed expression.
# When used in the function `cse()`, the target expressions will be transformed
# by each of the preprocessor functions in order. After the common
# subexpressions are eliminated, each resulting expression will have the
# postprocessor functions transform them in *reverse* order in order to undo the
# transformation if necessary. This allows the algorithm to operate on
# a representation of the expressions that allows for more optimization
# opportunities.
# `None` can be used to specify no transformation for either the preprocessor or
# postprocessor.
cse_optimizations = list(cse_opts.default_optimizations)

def numbered_symbols(prefix='x'):
    """ Generate an infinite stream of Symbols consisting of a prefix and
    increasing subscripts.

    Parameters
    ----------
    prefix : str, optional
        The prefix to use. By default, this function will generate symbols of
        the form "x0", "x1", etc.

    Yields
    ------
    sym : Symbol
        The subscripted symbols.
    """
    i = 0
    while True:
        name = '%s%s' % (prefix, i)
        yield Symbol(name)
        i += 1

def preprocess_for_cse(expr, optimizations):
    """ Preprocess an expression to optimize for common subexpression
    elimination.

    Parameters
    ----------
    expr : sympy expression
        The target expression to optimize.
    optimizations : list of (callable, callable) pairs
        The (preprocessor, postprocessor) pairs.

    Returns
    -------
    expr : sympy expression
        The transformed expression.
    """
    for pre, post in optimizations:
        if pre is not None:
            expr = pre(expr)
    return expr

def postprocess_for_cse(expr, optimizations):
    """ Postprocess an expression after common subexpression elimination to
    return the expression to canonical sympy form.

    Parameters
    ----------
    expr : sympy expression
        The target expression to transform.
    optimizations : list of (callable, callable) pairs, optional
        The (preprocessor, postprocessor) pairs.  The postprocessors will be
        applied in reversed order to undo the effects of the preprocessors
        correctly.

    Returns
    -------
    expr : sympy expression
        The transformed expression.
    """
    if optimizations is None:
        optimizations = cse_optimizations
    for pre, post in reversed(optimizations):
        if post is not None:
            expr = post(expr)
    return expr

def cse(exprs, symbols=None, optimizations=None):
    """ Perform common subexpression elimination on an expression.

    Parameters:

    exprs : list of sympy expressions, or a single sympy expression
        The expressions to reduce.
    symbols : infinite iterator yielding unique Symbols
        The symbols used to label the common subexpressions which are pulled
        out. The `numbered_symbols` generator is useful. The default is a stream
        of symbols of the form "x0", "x1", etc. This must be an infinite
        iterator.
    optimizations : list of (callable, callable) pairs, optional
        The (preprocessor, postprocessor) pairs. If not provided,
        `sympy.simplify.cse.cse_optimizations` is used.

    Returns:

    replacements : list of (Symbol, expression) pairs
        All of the common subexpressions that were replaced. Subexpressions
        earlier in this list might show up in subexpressions later in this list.
    reduced_exprs : list of sympy expressions
        The reduced expressions with all of the replacements above.
    """
    if symbols is None:
        symbols = numbered_symbols()
    else:
        # In case we get passed an iterable with an __iter__ method instead of
        # an actual iterator.
        symbols = iter(symbols)
    seen_subexp = set()
    to_eliminate = []

    if optimizations is None:
        # Pull out the default here just in case there are some weird
        # manipulations of the module-level list in some other thread.
        optimizations = list(cse_optimizations)

    # Handle the case if just one expression was passed.
    if isinstance(exprs, Basic):
        exprs = [exprs]
    # Preprocess the expressions to give us better optimization opportunities.
    exprs = [preprocess_for_cse(e, optimizations) for e in exprs]

    # Find all of the repeated subexpressions.
    for expr in exprs:
        for subtree in postorder_traversal(expr):
            if subtree.args == ():
                # Exclude atoms, since there is no point in renaming them.
                continue
            if (subtree.args != () and
                subtree in seen_subexp and
                subtree not in to_eliminate):
                to_eliminate.append(subtree)
            seen_subexp.add(subtree)

    # Substitute symbols for all of the repeated subexpressions.
    replacements = []
    reduced_exprs = list(exprs)
    for i, subtree in enumerate(to_eliminate):
        sym = symbols.next()
        replacements.append((sym, subtree))
        # Make the substitution in all of the target expressions.
        for j, expr in enumerate(reduced_exprs):
            reduced_exprs[j] = expr.subs(subtree, sym)
        # Make the substitution in all of the subsequent substitutions.
        # WARNING: modifying iterated list in-place! I think it's fine,
        # but there might be clearer alternatives.
        for j in range(i+1, len(to_eliminate)):
            to_eliminate[j] = to_eliminate[j].subs(subtree, sym)

    # Postprocess the expressions to return the expressions to canonical form.
    for i, (sym, subtree) in enumerate(replacements):
        subtree = postprocess_for_cse(subtree, optimizations)
        replacements[i] = (sym, subtree)
    reduced_exprs = [postprocess_for_cse(e, optimizations) for e in reduced_exprs]

    return replacements, reduced_exprs

def cse_full(eq):
    """Get a fully substituted expression from cse."""
    du=Symbol('x',dummy=True)
    r,e=cse(eq+eq*du)
    return r, e[0].coeff(du)

def polify(eq, debug=0):
    """Return list of replacements and polynomial-like eq.args

    Since factoring cannot (at present) cannot be done with polys, this
    is a work around which replaces items that would cause problems to the
    polys routines. All non-integer exponents and any non-number and non-symbol
    coefficients are replaced with symbols.

    The eq returned will either be a fraction with cancelled terms or else a
    non-rational expression. The replacements will be in reverse numerical
    order so a backsubstitution can be done directly as shown below.

    Examples::

    >>> polify(exp(2*a*x)*x+x**2*exp(a*x/2)+x**3*exp(x/3)+x*(I+pi))
    ([(x5, x0**(1/6)), (x4, x1**(1/2)), (x3, I), (x2, pi), (x1, exp(a)), (x0, exp(x))],
    x*(x2 + x3 + x**2*x5**2 + x*x4*x5**3 + x4**4*x5**12))

    >>> r, e = polify((exp(x)+exp(-x))/(exp(x)-exp(-x)))
    ([(x0, exp(x))], -(1 + x0**2)/((1 + x0)*(1 - x0)))
    >>> e.subs(r)
    -(1 + exp(2*x))/((1 - exp(x))*(1 + exp(x)))

    Note: Whereas cse is exhaustive in its replacements, this routine just
    replaces those that would cause problems to polys. Thus, much of the
    structure, especially factorable structure, remains.

    """

    sfarm = numbered_symbols() #symbol generator
    def snew(f):
        """
        Find the next numeric symbol from sfarm that can be used in the
        expression without resorting to dummy variables.

        """

        while 1:
            s=sfarm.next()
            if s not in f.args:
                return s

    def valence(eq):
        """
        Return the top-level arguments of an expression up to the
        powers (other than X**-1) and functions.

        """

        got=[]
        todo=[eq]
        #drill down to the function and power level
        while todo:
            eq=todo.pop()
            if eq.is_Atom or eq.is_Function or (eq.is_Pow and eq.exp!=-1):
                got.append(eq)
            else:
                for tmp in eq.args:
                    if eq.is_Pow and tmp==-1:continue
                    todo.append(tmp)
        return set(got)


    def gremlins(eq):
        """
        Return those items that will cause problems to factor():
        arguments that aren't numbers or symbols, and arguments
        that are powers with non-integer exponents.

        """

        baduns = set([])
        for x in valence(eq):
            if x.is_Number or x.is_Symbol:
                continue
            if x.is_Pow:
                if x.base.is_Symbol and x.exp.is_Integer:
                    continue
                if x.exp.is_Integer:
                    x=x.base
            baduns.add(x)
        return baduns

    eq=sympify(eq)
    reps=[]
    p=Symbol('p',dummy=True,positive=True)

    #clear number symbols and irrationals
    baduns = set(n for n in gremlins(eq) if \
                 n.is_NumberSymbol or \
                 n==S.ImaginaryUnit or \
                 n.is_Pow and n.base.is_Number and n.exp.is_Number and not n.exp.is_Integer) #3**(1/sqrt(2)), 3**sqrt(2)
    if debug: print 'number-like things',baduns
    for bad in baduns:
        tmp=snew(eq)
        eq=eq.subs(bad,tmp)
        reps.append((tmp,bad))

    #powers with symbol arguments (including exp())
    eq=eq.expand()
    terms = [tmp for tmp in gremlins(eq) if
             tmp.func==exp and tmp.atoms(Symbol) or
             tmp.is_Pow and (tmp.exp.atoms(Symbol) or gremlins(tmp.exp))]
    if debug: print 'power terms',terms
    rterms=[[S.One,
             tmp.base if tmp.is_Pow else S.Exp1,
             tmp.exp if tmp.is_Pow else tmp.args[0]]
            for tmp in terms]
    bdict = {}
    for term in terms:
        if term.is_Function:
            assert term.func is exp
            b=S.Exp1
            e=term.args[0]
            be=[(b,e)]
        else:
            be=[term.args]
        for b,e in be:
            if b not in bdict:
                bdict[b]=set([])
            bdict[b].add(e)
    for b,eargs in bdict.items():
        for vi in eargs:
            if vi.is_Number:
                continue
            tmp=snew(eq)
            reps.append((tmp,b**vi))
            #eq=eq.subs(b**vi) this fails on (a**b*a**(c*x/a)).subs(a**(c*x),y)
            for i,(repl,ba,ex) in enumerate(rterms):
                if b == ba:
                    if not vi in ex:continue
                    rterms[i][0]*=tmp
                    rterms[i][2]/=vi
    for i,t in enumerate(terms):
        repl,ba,ex=rterms[i]
        eq=eq.subs(t,p**ex).subs(p,repl)

    #clear all other functions
    baduns = set(n for n in gremlins(eq) if n.is_Function)
    if debug: print 'bad functions',baduns
    for bad in baduns:
        tmp=snew(eq)
        eq=eq.subs(bad,tmp)
        reps.append((tmp,bad))

    #clear rational exponents on terms
    rpows = [tmp for tmp in gremlins(eq) if tmp.is_Pow and tmp.exp.as_numer_denom()[1]!=1]
    if debug: print 'rational powers',rpows
    bases=set(tmp.base for tmp in rpows)
    for b in bases:
        expos=list(tmp.exp.as_numer_denom()[1] for tmp in rpows if tmp.base is b)
        q=reduce(ilcm,expos)
        if q==1:continue
        sym=snew(eq)
        reps.append((sym,b**Rational(1,q)))
        eq=eq.subs(b,p**q).subs(p,sym) #p is being used to get powers to combine (x**1/2)**2 -> x

    n,d = eq.as_numer_denom()
    try:
        eq=factor(n)/factor(d)
    except:
        print 'there was something that did not get replaced in following num and den'
        print 'num:',n
        print 'den:',d
        assert None

    return list(reversed(reps)),eq
