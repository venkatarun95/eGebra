import sympy

import sympy_computation_list

import error_reporter

'''This is the sympy specific section. Change if you want to change the back end'''
#interface with sympy_computations.py to get the function
def getFunction(keyStr):
    return sympy_computation_list.getFunction(keyStr)

class compTypeEnum(object):
    newObject = 1
    newProperty = 2

#Format:
#  -Name with which the action is reffered to (the key)

#  -Some verbose description of the action
#  -Type of result from computation (creates an object(1)/property(2))
#  -Number of arguments the action takes
#  -Verbose descriptions of the arguments
generic_computation_description = {
    'S-simplify': ('Try to automatically simplify the expression', compTypeEnum.newObject, 1, 'The expression to simplify'),
    'S-expand': ('Expand any bracketed powers within the expression', compTypeEnum.newObject, 1, 'The expression to expand'),
    'S-cancel': ('Cancel common terms in numerator and denominator of an expression', compTypeEnum.newObject, 1, 'The expression over which to operate'),
    'S-break into partial fractions': ('Break an expression into partial fractions', compTypeEnum.newObject, 1, 'The expression to break'),
    'S-take fractions together': ('Bring various fractions together into one. Opposite of \'break into partial fractions\'', compTypeEnum.newObject, 1, 'The expression to operate on'),
    'S-differentiate': ('Take the partial derivative/differentiate of the expression', compTypeEnum.newProperty, 2, 'The expression to differentiate', 'The variable to differentiate against')
}

def getComputationDescription(keyStr):
    '''Retreives the relevant record from the database'''
    if keyStr in generic_computation_description:
        return generic_computation_description[keyStr]
    else:
        error_reporter.reportProgramError("sympy_actions.py:getFunction :- Cannot find an entry with the given key: \'"+keyStr+"\'")
        exit()

def getNoArgs(keyStr):
    '''return the number of arguments for a particular computation given th e key string'''
    assert(type(getComputationDescription(keyStr)[2]) is int)
    return getComputationDescription(keyStr)[2]

def getComputationType(keyStr):
    assert(type(getComputationDescription(keyStr)[1]) is int)
    return getComputationDescription(keyStr)[1]

#returns all possible computations in a uniform format for sending to front end etc.
def getPossibleComputations():
    res = {}
    for comp in generic_computation_description:
        data = generic_computation_description[comp]
        res[comp] = {"descr":data[0], "compType":data[1], "noArgs":data[2], "argsDescr": data[3:]}
    return res