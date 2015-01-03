import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token

import cas_manager

#=====SENDING PAGES=====

def login_page(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['notebookId'] = 1 #Warning: Default notebook 1 until this feature is more completely implemented
				return redirect('/egebra/notebook_viewer')
			else:
				return render(request, 'login.html', {"error_message": 'Sorry your account has been disabled.'})
		else:
			return render(request, 'login.html', {"error_message": 'Atleast one of the given username and password is incorrect.'})
	elif request.method == 'GET':
		return render(request, 'login.html')

def logout_page(request):
	logout(request)
	return redirect('/egebra/login')

#@csrf_protect
@login_required
def notebook_viewer_page(request):
	return render(request, 'notebook_viewer.html')

'''url(r'cas_request/listen', views.listen_request, name='listen_request'),
url(r'cas_request/createSymbolicObject', views.create_symbolic_object_request, name='create_symbolic_object_request'),
url(r'cas_request/requestComputation', views.request_computation_request, name='request_computation_request'),
url(r'cas_request/requestListOfPossibleComputations', views.list_of_possible_computations_request, name="list_of_possible_computations"),
'''

#=====HANDLING REQUESTS=====
#Naming convention: post request like this are named as camelCase_request. Requests for pages are named as camel_case_request
#Refer README for full details of naming conventions
#Warning: Does this (ie. using csrf_exempt) open up any security loopholes?
#@csrf_protect
@login_required
@csrf_exempt
@requires_csrf_token
def listen_request(request):
	#print("Listen request")
	#assert(False)
	if request.method == 'GET':
		return HttpResponse('{"msg": "Error: Undefined behaviour for GET request at this url"}', mimetype="application/json")
	return HttpResponse('{"msg": "NothingYet"}', mimetype="application/json")	
	#return HttpResponse(json.dumps({"msg": "New object available", "obj": ("diff", "x")}), mimetype="application/json")

@login_required
@csrf_exempt
@requires_csrf_token
def createSymbolicObject_request(request):
	try:
		if not request.session.get('notebookId'):
			return HttpResponse("{\"msg\": \"Error: Notebook Id not specified. Please report this to the developers.\"}", content_type="application/json")
		notebookId = request.session['notebookId']
		requestString = str(request.POST.dict()['requestData'])
		
		try:
		    requestData = json.loads(requestString)
		    symbolStr, stringLang = requestData["symbolStr"].encode('ascii', 'ignore'), requestData["stringLang"].encode('ascii', 'ignore')
		except:
		    return HttpResponse("{\"msg\": \"Error: Incorrect format of JSON object.\"}", content_type="application/json")
		
		try:
		    res=cas_manager.cas_manager_interface.createSymbolicObject(symbolStr, stringLang, notebookId)
		except:
			cas_manager.error_reporter.reportRuntimeWarning("views.py.createSymbolicObject: Error while creating symbol")
			#Warning: should never be reached because of error_reporter
			return HttpResponse("{\"msg\": \"Error while creating symbol.\"}", mimetype="application/json")
		return HttpResponse("{\"msg\": \"Symbol creation successful.\", \"symObj\":"+json.dumps(res.getRepresentativeObject())+"}", mimetype="application/json")
	except:
		cas_manager.error_reporter.reportRuntimeProgramError("Unhandled error.")
		return HttpResponse("{\"msg\": \"Error: Unhandled error.\"}", content_type="application/json")

@login_required
@csrf_exempt
@requires_csrf_token
def requestComputation_request(request):
	try:
		try:
			requestString = str(request.POST.dict()['requestData'])
			requestData = json.loads(requestString)
			keyStr, symObjKeys = requestData["keyStr"].encode('ascii', 'ignore'), requestData["symObjKeys"]
		except:
			self.wfile.write("Error: Incorrect format of JSON object.")
			return
		try:
			cas_manager.cas_manager_interface.pushComputation(keyStr, symObjKeys, 100) #priority 100 as it is from the user (super high priority)
		except:
			return HttpResponse('{"msg": "Error: Error while pushing computation. Please report this."}', mimetype="application/json")
		return HttpResponse('{"msg": "Computation push successful."}', mimetype="application/json")
	except:
		cas_manager.error_reporter.reportRuntimeProgramError("Unhandled error.")
		return HttpResponse("{\"msg\": \"Error: Unhandled error.\"}", content_type="application/json")
