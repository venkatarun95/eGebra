from symbolic_object_sympy import symPySymbolicObject as sobjSP

class symbolicObject:
    '''Wrapper for symPySymbolicObject in symbolic_object_sympy. Simply calls its functions whenever required'''
    
    def __init__(self, exprStringOrObj, exprStringType=None):
        #jugaad for function overloading
    	if exprStringType == None:
    	    self.symObj = sobjSP(exprStringOrObj)
    	else:
            self.symObj = sobjSP(exprStringOrObj, exprStringType)

    def setKeyID(self, keyID):
    	self.symObj.setKeyID(keyID)

    def getKeyID(self):
        return self.symObj.getKeyID()

    def getComputableObject(self):
        return self.symObj.getComputableObject()

    def addProperty(self, nameKey, associatedObjectKeys, result):
        self.symObj.addProperty(nameKey, associatedObjectKeys, result)

    def addInRelation(self, keyStr, referenceTo):
    	self.symObj.addInRelation(keyStr, referenceTo)
    
    def addOutRelation(self, keyStr, referenceTo):
    	self.symObj.addOutRelation(keyStr, referenceTo)

    def getRepresentativeObject(self):
        return self.symObj.getRepresentativeObject()