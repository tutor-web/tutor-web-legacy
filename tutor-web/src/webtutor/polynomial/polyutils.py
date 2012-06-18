# -*- coding: latin-1 -*-
# Above comment specifies unicode encoding
from __future__ import print_function
import sympy
from numpy.random import random_integers


def getPoly(order, sym=sympy.symbols('x')):
    roots = random_integers(-5,5, order)
    leadCoeff = random_integers(1,5)
    poly = sympy.S(leadCoeff)
    for root in roots:
        poly *= sym-root
    return sympy.Poly(poly.expand())

def getSols(poly, sym, orderDiff):
    df = poly
    polyDiffs = []
    diffRoots = []
    for i in range(1+orderDiff):
        polyDiffs += [df]
        roots = sympy.roots(df)
        diffRoots += [roots]
        df = df.diff()
    return polyDiffs, diffRoots

def getRealPoly(order, orderDiff, sym=sympy.symbols('x')):
    poly = getPoly(order, sym)
    polyDiffs, diffRoots = getSols(poly, sym, orderDiff)
    # Keep making polynomials until we get one with all real roots
    for roots in diffRoots:
        for root in roots:
            if not sympy.ask(sympy.Q.real(root)):
                return getRealPoly(order, orderDiff, sym)
    return polyDiffs, diffRoots

if __name__ == '__main__':
    polyDiffs, diffRoots = getRealPoly(4, 3)
    for i in range(len(polyDiffs)):
        print(u'{i}° derivative:\n{poly}\n\nroots:'.format(i=i,poly=sympy.pretty(polyDiffs[i].as_expr())))
        for root in diffRoots[i]:
            print(sympy.pretty(root))
        print()