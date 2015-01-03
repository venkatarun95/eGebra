symObjs = []
symObjEdges = []

listenForComputationResult = function(){
	$.post("/listen", "", function(response){
		//console.log(response)
		if("message" in response)
			; //ie. no new result has arrived
		else{
			//Store it
			if(response.startsWith("Error:")){
				console.log(response)
				alert("There was an error while creating the symbol. Please check the syntax.")
			}
			symObjs.push(response[1])
			//Add it
			document.getElementById("ObjectDisplay").innerHTML += "<div id=\"object"+response[1]["keyID"]+"\" style=\"position:absolute\">\\["+response[1].latex+"\\]</div>"
			MathJax.Hub.Queue(["Typeset",MathJax.Hub,"object"+response[1]["keyID"]]); //so that MathJax typesets it again
			//link it to the graph
			graphHandler.addGraphNode("object"+response[1]["keyID"])
			//graphSys.addNode("object"+response[1]["keyID"], response)
			for(x in response[1]["inRelation"]){
				for(y in response[1]["inRelation"][x]){
					graphSys.addEdge("object"+response[1]["keyID"], "object"+response[1]["inRelation"][x][y])
					//create the relevant HTML so that it can be displayed
					document.getElementById("EdgeDisplay").innerHTML += "<div id=\""+"object"+response[1]["keyID"]+"object"+response[1]["inRelation"][x][y]+"\" style=\"position:absolute;\">"+x+"</div>"
				}
			}
		}
	});
}

createSymbolObject = function(symbolStr){
	$.post("/createSymbolObject", "{\"symbolStr\": \""+symbolStr+"\", \"stringLang\": \"sympy\"}", function(response){
		if(response["message"] != "Symbol creation successful."){
			console.log("Error: Error while creating symbol: "+symbolStr)
			return
		}
		//Store it
		symObjs.push(response.symObj)
		//Add it to graph
		document.getElementById("ObjectDisplay").innerHTML += "<div id=\"object"+response.symObj.keyID+"\" style=\"position:absolute\">\\["+response.symObj.latex+"\\]"
		MathJax.Hub.Queue(["Typeset",MathJax.Hub,"object"+response.symObj.keyID]); //so that MathJax typesets it again
		graphHandler.addGraphNode("object"+response.symObj.keyID)
	});
}

var possibleComputations
getListOfPossibleComputations = function(){
	$.post("/requestListOfPossibleComputations", "", function(response){
		possibleComputations = response
		res = ""
		for(x in response){
			//res += "<options value=\""+x+"\"><i>"+x+"</i>"+response[x].descr+"</options>"
			document.getElementById("possibleComputationsListID").options.add(new Option(response[x].descr, x))
		}

		//add some extra special-operations defined by the client
		document.getElementById("possibleComputationsListID").options.add(new Option("Create a new symbolic object", "Spl-create symbolic object"))
	})
}

var requestComputation = function(keyStr, symObjKeys){
	$.post("/requestComputation", "{\"keyStr\": \""+keyStr+"\", \"symObjKeys\": "+symObjKeys+"}", function(response){
		if(response != "Computation push successful."){
			console.log(response)
			console.log("/requestComputation", "{\"keyStr\": \""+keyStr+"\", \"symObjKeys\": "+symObjKeys+"}")
		}
	});
}

$(document).ready(function(){
	//alert("Document is ready");
	getListOfPossibleComputations()
	//createSymbolObject("sin(x)**2+cos(x)**2")
	//createSymbolObject("(sin(x)+cos(x))**2")


	/*$.post("/requestComputation", "{\"keyStr\": \"S-simplify\", \"symObjKeys\": [1]}", function(response){
		console.log(response)
		graphSys
	});
	$.post("/requestComputation", "{\"keyStr\": \"S-expand\", \"symObjKeys\": [2]}", function(response){
		console.log(response)
	});
	$.post("/requestComputation", "{\"keyStr\": \"S-simplify\", \"symObjKeys\": [4]}", function(response){
		console.log(response)
	});*/

	setInterval(listenForComputationResult, 2000)
	/*listenForComputationResult()
	listenForComputationResult()
	listenForComputationResult()
	listenForComputationResult()*/
});

/*$.get("liste", function(response){
	alert("Response received!" + response)
	console.log(response);
});*/

/*$.post("/createSymbolObject", "{\"symbolStr\": \"sin(x)**2+cos(x)**2\", \"stringLang\": \"sympy\"}", function(response){
	//alert("POST response: " + response);
	});
$.post("/createSymbolObject", "{\"symbolStr\": \"(sin(x)+cos(x))**2\", \"stringLang\": \"sympy\"}", function(response){
	//alert("POST response: " + response);
	});*/