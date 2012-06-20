import rpy2.robjects as robj
import numpy.random as rand
from collections import Counter

def seed(x):
    rand.seed(x)
    robj.r('set.seed(%i)' % x)


def sample(x, size=1, replace=False, p=None):
    ''' Mask for corresponding R function.'''
    x = list(x)
    indices = robj.IntVector(range(len(x)))
    if p is not None:
        p_R = robj.FloatVector(p)
    else:
        p_R = robj.NULL
    sampleIndices = robj.r.sample(indices, size, replace, p_R)
    if size == 1:
        return x[sampleIndices[0]]
    else:
        return [x[i] for i in sampleIndices]

def _getFraction(num, den):
    pass
    

def fractions(size=1, replace=False, numerators=[1,2,3,5,7], denominators=[1,2,3,5,7]):
    ''' Returns randomly generated sympy Fractions.
    Guaranteed to be not an integer.'''
    # Make sure it's guaranteed to get a fraction, i.e.,
    # numerators and denominators are not all the same number,
    # and denominators is not just 1.
    cNums = Counter(numerators)
    cDens = Counter(denominators)
    nks = cNums.keys()
    dks = cDens.keys()
    if (len(nks) == 1 and len(dks) == 1 and dks == nks) or (len(dks) == 1 and dks[0] == 1):
        raise ValueError('Impossible to create a fraction with given numerators and denominators.')
    # Make sure 1 isn't in there
    cDens.pop(1)
    if not replace: # Make sure it is possible to generate enough fractions
        pass
    print cDens
    denominators = list(cDens)
    nums = sample(numerators, size, replace)
    dens = sample(denominators, size, replace)
    # Have to generate fractions so that there aren't any integers
    cNums = Counter(nums)
    cDens = Counter(dens)
    print cNums, cDens
    # Make sure that it's possible to not have any integers
    numKeys = cNums.keys()
    denKeys = cDens.keys()
    for nk in numKeys:
        # If there are not enough possible denominators that are not
        # nk, then it is not possible to not make an integer
        pass
    

if __name__ == '__main__':
    a = ['Sample %s' % i for i in range(1,11)]
    p = [i for i in range(1,11)]
    print sample(a, 4, True, p)
    for f in fractions(5, True):
        print f
