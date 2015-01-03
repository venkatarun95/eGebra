def reportProgramError(errStr):
    print "Program Error: " + errStr
    print "Program will now terminate..."
    exit()

def reportRuntimeWarning(errStr):
    print "Runtime Warning: " + errStr

def reportRuntimeProgramWarning(errStr):
	print "Program Runtime Warning: " + errStr
	print "Program will try to continue execution..."