import sympy

import symbolic_object_sympy
import symbolic_object
import generic_cas_computations

import error_reporter

sympy_action_implementation = {
           'S-simplify': sympy.simplify,
           'S-expand': sympy.expand,
           'S-cancel': sympy.cancel,
           'S-break into partial fractions': sympy.apart,
           'S-take fractions together': sympy.together,
           'S-differentiate': sympy.diff}

def getFunction(keyStr):
    if keyStr in sympy_action_implementation:
          noArgs = generic_cas_computations.getNoArgs(keyStr)
          if noArgs == 1:
              return lambda x: symbolic_object.symbolicObject(sympy_action_implementation[keyStr](x.getComputableObject()))
          elif noArgs == 2:
            return lambda x, y: symbolic_object.symbolicObject(sympy_action_implementation[keyStr](x.getComputableObject(), y.getComputableObject()))
          else:
            error_reporter.reportProgramError("sympy_actions.py:getFunction :- An unhandled number of arguments are required: "+noArgs)
    else:
        error_reporter.reportProgramError("sympy_actions.py:getFunction :- Cannot find an entry with the given key: \'"+keyStr+"\'")