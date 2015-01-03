btnComputationQueryHandler = function(){
    selObj = document.getElementById(selectHTMLID)
    if(selObj.value.startsWith("Spl-")){	//special case, needs to be handled separately
		if(selObj.value == "Spl-create symbolic object"){
			inpStr = document.getElementById(inpArgsNewSymbolHTMLID).value
			computationHandler.createNewSymbolicObject(inpStr)
		}
		else
			console.log("Special operation '"+selObj.value+"' not recognised")
	}
	else{
		selObjs = graphHandler.getSelectedSymObjs()
		computationHandler.requestNewComputation(selObj.value, selObjs)
	}
}

expandCanvas = function(){
	document.getElementById('symObjDisplay').height+=100
	//update the coordinated in the graph manager
	graphHandler.updateGraphDimensions()
}

contractCanvas = function(){
	if(document.getElementById('symObjDisplay').height > 100){
		document.getElementById('symObjDisplay').height -= 100
		//update the coordinated in the graph manager
		graphHandler.updateGraphDimensions()
	}
	else
		alert("Please don't make the size negative!")
}

var selectHTMLID = "possibleComputationsListID"
var argSelectorSidePanelID = "SidePanelArgumentSelector"
var inpArgsNewSymbolHTMLID = "InpArgsNewSymbol"
$(document).ready(function(){
	$("#possibleComputationsListID").change(function(){
		uiHandler.updateArgsSelectionSidebar()
	})
})

//view to the external javascript world
var uiHandler = {
	updateArgsSelectionSidebar:function(){
		selObj = document.getElementById(selectHTMLID)

		if(selObj.value.startsWith("Spl-")){	//special case, needs to be handled separately
			if(selObj.value == "Spl-create symbolic object"){
				resStr = "Enter the new symbolic object: <input type='text' id='"+inpArgsNewSymbolHTMLID+"'></input>"
				$("#"+argSelectorSidePanelID).html(resStr)
				graphHandler.setNoSymObjsToSelect(0)
			}
			else
				console.log("Special operation '"+selObj.value+"' not recognised")
			return
		}
		args = computationHandler.getArgsDescr(selObj.value)
		selObjs = graphHandler.getSelectedSymObjs()

		resStr=""
		for(x in args){
			if(x < selObjs.length)
				resStr += "<p>"+args[x]+": \\["+computationHandler.getLatex(selObjs[x])+"\\]</p>"//<input type=\"text/html\" id=\"txtInpArgSelection\" value=\"\"></input></p>"
			else 
				resStr += "<p>"+args[x]+": <i>Please select a symbol</i></p>"
		}
		$("#"+argSelectorSidePanelID).html(resStr)
		MathJax.Hub.Queue(["Typeset",MathJax.Hub,argSelectorSidePanelID]); //so that MathJax typesets it again

		//tell the graph handler about the number of symbols to select
		graphHandler.setNoSymObjsToSelect(args.length)
	}
}