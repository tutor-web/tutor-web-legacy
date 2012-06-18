from webtutor import polynomial as poly
from webtutor import MCQuestionGenerator as MCQGen
import sympy as sym

polyDiffs, diffRoots = poly.getRealPoly(4,2)

intro = '''Consider the polynomial $p(x)={}$.'''.format(sym.latex(polyDiffs[0]))
questions = ['What is the degree of $p$?',
             'Which of the following are roots of $p$?',
             'What is the derivative of $p$?',
             "What is the degree of $p'$?",
             'Which of the following are critical points of $p$?',
             'What is the second derivative $p$?',
             "What is the degree of $p''$?",
             'Which of the following are inflection points of $p$?']
questions = ['{}\n\n{}'.format(intro, q) for q in questions]
# Make as many titles as there are questions
title = ['poly' for i in range(len(questions))]
answers = []
# Generate the answers
for i in range(len(polyDiffs)):
    poly = polyDiffs[i]
    roots = diffRoots[i]
    rootsTex = [sym.latex(root) for root in roots]
    polyTex = sym.latex(poly)
    if i != 0: # The zeroth order derivative is given
        answers.append(['${}$.'.format(polyTex)])
    answers.append(['${}$.'.format(poly.degree())])
    answers.append(['${}$.'.format(rootTex) for rootTex in rootsTex])
# Generate the explanations
diffExplan = """Remember that differentiation is a linear operator, \
which means $((f(x)+g(x))'=f'(x)+g'(x)$. So we can differentiate ${}$ \
by taking the derivative of each term individually.
Hint: $(ax^n)'=nax^{{n-1}}$ when $n$ is not zero.""".format(sym.latex(polyDiffs[0]))
degExplan = """A polynomial has the same degree as the highest degree of its terms, \
and the degree of each term is simply the number in its exponent. So the degree \
of a polynomial is the value of the biggest exponent which appears in it."""
rootExplan = '''The roots of a polynomial can be found with the following procedure:'''
critPtExplan = "The critical points of a function are the zeroes (roots) of the function's derivative."
infPtExplan = "The inflection points of a function are the zeroes (roots) of the function's second derivative."
explanations = []
# Generate the explanations
for i in range(len(polyDiffs)):
    expStr = ''
    