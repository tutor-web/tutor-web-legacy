import rpy2.robjects as robj
import numpy.random as rand

def seed(x):
    rand.seed(x)
    robj.r('set.seed(%i)' % x)


def sample(x, size=1, replace=False, p=None):
    ''' Mask for corresponding R function.'''
    indices = robj.IntVector(range(len(x)))
    if p is not None:
        p_R = robj.FloatVector(p)
    else:
        p_R = robj.NULL
    sampleIndices = robj.r.sample(indices, size, replace, p_R)
    return [x[i] for i in sampleIndices]

def _getFraction(numerators, denominators):
    # Make sure it's possible to get a fraction that
    # is not an integer.
    num = sample(numerators)
    den = sample(denominators)
    

def fraction(size=1, replace=False, numerators=[1,2,3,5,7], denominators=[2,3,5,7]):
    ''' Returns randomly generated sympy Fractions.
    Guaranteed to be not an integer.'''
    

if __name__ == '__main__':
    a = ['Sample %s' % i for i in range(1,11)]
    p = [i for i in range(1,11)]
    print sample(a, 4, True, p)
