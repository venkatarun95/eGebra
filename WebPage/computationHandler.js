//Note: many variables referenced in this file are defined and maintained in communicator.js

var computationHandler = {
	getArgsDescr:function(keyStr){
		//possibleComputations comes from communicator.js
		return possibleComputations[keyStr].argsDescr
	},

	getLatex:function(objID){
		for(x in symObjs){
			if(symObjs[x].keyID==objID)
				return symObjs[x].latex; //defined and maintained by communicator.js
		}
		return "Error: Object not found. Please report this"
	},

	createNewSymbolicObject:function(symStr){
		createSymbolObject(symStr)	//function defined in communicator.js
	},

	requestNewComputation:function(keyStr, symObjKeys){
		requestComputation(keyStr, JSON.stringify(symObjKeys[0]))	//function defined in communicator.js
	}
}