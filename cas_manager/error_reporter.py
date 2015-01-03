import traceback

def reportProgramError(errStr):
    print "Program Error: " + errStr
    print "Program will now NOT terminate..."
    print(traceback.format_exc())
    #exit()

def reportRuntimeWarning(errStr):
    print "Runtime Warning: " + errStr
    print(traceback.format_exc())

def reportRuntimeProgramWarning(errStr):
	print "Program Runtime Warning: " + errStr
	print "Program will try to continue execution..."
	print(traceback.format_exc())