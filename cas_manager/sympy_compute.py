import sympy

import generic_cas_computations
import symbolic_object_list

import error_reporter

def computeAndReturn(keyStr, args):
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


def computeAndModify(keyStr, symObjKeys):
    symObjs = map(symbolic_object_list.getObj, range(len(symObjKeys)))
    res = compute(keyStr, symObjs)
    computationType = getComputationType(keyStr)
    if computationType == symbolic_object_list.compTypeEnum.newObject:
        symbolic_object_list.addObj(res)
    elif computationType = symbolic_object_list.compEnumType.newProperty:
        for sObj in symObjKeys:
            sObj.addProperty(keyStr, symObjKeys, res)
    

#x = sympy.Symbol('x')
#print compute('S-break into partial fractions', [sympy.sin(x)**2 + sympy.cos(x)**2 + 2*sympy.sin(x)*sympy.cos(x)])
