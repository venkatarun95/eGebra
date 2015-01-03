import sympy
import copy

import generic_cas_computations
from symbolic_object_list import symbolic_object_list

import error_reporter

def computeResult(keyStr, args):
    '''Calls the relevant function to perform the computation.

        @param keyStr - the key string identifying the computation (operation)
        @param args - the keys of the object on which to apply the computation'''
    noArgs = generic_cas_computations.getNoArgs(keyStr)

    if len(args) > 2:
        error_reporter.reportProgramError("sympy_act.py:compute :- This function does not yet handle arguments of length greater than 2. noArgs = "+noArgs+", arge.length = "+len(args))
        return
    elif len(args) != noArgs:
        error_reporter.reportProgramError("sympy_act.py:compute :- Number of arguments given does not match expected number of arguments. noArgs = "+noArgs+", len(args) = "+len(args))
        return
    
    try:
        if noArgs == 1:
            return generic_cas_computations.getFunction(keyStr)(args[0]) #sympy_computation_list.getFunction(keyStr)(args[0])
        if noArgs == 2:
            return generic_cas_computations.getFunction(keyStr)(args[0], args[1]) #sympy_computation_list.getFunction(keyStr)(args[0], args[1])
    except NotImplementedError:
        return []

def compute(keyStr, symObjKeys):
    '''Calls computeResult and handles the result by appropriately creating a new object or property

        @param keyStr - the key string identifying the computation (operation)
        @param symObjKeys - the keys of the object on which to apply the computation
        @note all computations are done over a copy of the original object, not the object itself, so that multiple computations can run in parallel without a clash'''
    symObjs = map(lambda x:copy.deepcopy(symbolic_object_list.getObj(x)), symObjKeys)
    res = computeResult(keyStr, symObjs)

    updateWithResult(keyStr, symObjKeys, res)
    return res

def updateWithResult(keyStr, symObjKeys, res):
    computationType = generic_cas_computations.getComputationType(keyStr)
    if computationType == generic_cas_computations.compTypeEnum.newObject:
        symbolic_object_list.addObjectWithLinks(res, keyStr, symObjKeys)
    elif computationType == generic_cas_computations.compTypeEnum.newProperty:
        res.addInRelation(keyStr, symObjKeys)
        symbolic_object_list.addObject(res)
        for sObj in symObjKeys:
            symbolic_object_list.getObj(sObj).addProperty(keyStr, symObjKeys+[res.getKeyID()], res)
    else:
        error_reporter.reportProgramError("compute.py:updateWithResult :- Invalid type of computation. It is neither a newProperty nor a newObject.")

#x = sympy.Symbol('x')
#print compute('S-break into partial fractions', [sympy.sin(x)**2 + sympy.cos(x)**2 + 2*sympy.sin(x)*sympy.cos(x)])