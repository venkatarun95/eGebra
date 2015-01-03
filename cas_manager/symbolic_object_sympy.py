import sympy

from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.mathematica import mathematica
from sympy.parsing.maxima import parse_maxima

import error_reporter

class symPySymbolicObject:
    '''Wrapper for the actual symPy objects and their operations'''
    def __init__(self, exprStringOrObj, exprStringType="sympy"):
        '''Initializes the object using string in a specific format or from an object'''
        self.properties = {}
        self.inRelation = {}
        self.outRelation = {}
        #jugaad for function overloading
        if type(exprStringOrObj) is str:
            flag = False
            try:
                if exprStringType == 'sympy':
                    self.symObj = parse_expr(exprStringOrObj)
                    #Note: Can use transformations as given in http://docs.sympy.org/dev/modules/parsing.html to improve the generality of possible expressions
                elif exprStringType == 'mathematica':
                    self.symObj = mathematica(exprStringOrObj)
                elif exprStringType == 'maxima':
                    self.symObj = parse_maxima(exprStringOrObj)
                else:
                    flag = true
            except:
                raise Exception("Error in parsing \'"+exprStringType+"\' code: \'"+exprStringOrObj+"\'")   
                 
            if flag:
                    raise Exception("Currently parsing strings of type \'"+exprStringType+"\' has not been implemented for the symPy backend. Please use \'sympy\', \'mathematica\' or \'maxima\' syntax")
        else: #it is a sympy object directly
            self.symObj = exprStringOrObj

    def setKeyID(self, keyID):
        self.keyID = keyID

    def getKeyID(self):
        try:
            keyID = self.keyID
        except AttributeError:
            error_reporter.reportProgramError("symbolic_object_sympy.py:symPySymbolicObject:getKeyID :- Tried to access keyID before initializing it.")
        return keyID

    def getComputableObject(self):
        return self.symObj

    def addProperty(self, nameKey, associatedObjectKeys, result):
        if nameKey in self.properties:
            try:
                objID = self.symObjID
            except AttributeError:
                objID = None
            errorReporter.reportRuntimeWarning("symbolic_object_sympy.py:symPySymbolicObject:addProperty :- In symbolic object with ID "+objID+", property \'"+nameKey+"\' already exists. An attempt was made to add it again. associatedObjectKeys = \'"+associatedObjectKeys+"\', result=\'"+result+"\'.")
        else:
            self.properties[nameKey] = (associatedObjectKeys, result)

    def addInRelation(self, keyStr, referenceFrom):
        if keyStr in self.inRelation:
            if referenceFrom == self.inRelation:
                errorReporter.reportRuntimeProgramWarning("symbolic_object_sympy.py:symPySymbolicObject:addInRelation :- The exact same in-relation is being added again. Please check.")
            else:
                errorReporter.reportRuntimeProgramWarning("symbolic_object_sympy.py:symPySymbolicObject:addInRelation :- The same type of in-relation is being added again, but wiht a different set of objects. Will not add the new relation.")
        else:
            self.inRelation[keyStr] = referenceFrom

    def addOutRelation(self, keyStr, referenceTo):
        if keyStr in self.outRelation:
            if referenceTo == self.outRelation:
                error_reporter.reportRuntimeProgramWarning("symbolic_object_sympy.py:symPySymbolicObject:addOutRelation :- The exact same out-relation is being added again. Please check.")
            else:
                error_reporter.reportRuntimeProgramWarning("symbolic_object_sympy.py:symPySymbolicObject:addOutRelation :- The same type of out-relation is being added again, but wiht a different set of objects. Will not add the new relation.")
        else:
            self.outRelation[keyStr] = referenceTo  

    def getRepresentativeObject(self):
        '''Returns a dictionary/list object that contains information about this symbolic object
           and can be transmitted to the front end for user interaction'''
        res = {}
        res["latex"] = sympy.latex(self.symObj)
        res["properties"] = self.properties
        res["inRelation"] = self.inRelation
        res["outRelation"] = self.outRelation
        res["keyID"] = self.getKeyID()
        return res