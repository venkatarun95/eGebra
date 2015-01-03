import cas_manager.symbolic_object
from cas_manager.symbolic_object_list import symbolic_object_list
import cas_manager.compute
import cas_manager.scheduler
import cas_manager.cas_manager_interface

import server

#Call the various initializers
symbolic_object_list.initialize()

def computationScheduler():
	return eatComputations

try:
	eatComputations = cas_manager.scheduler.scheduler()
	eatComputations.start()

	cas_manager.cas_manager_interface.initialize(eatComputations)

	serverObj = server.server()
	serverObj.setDaemon(True)
	serverObj.start()
except KeyboardInterrupt, SystemExit:
    print '^C received, shutting down the web server'
    exit()

#'''symbolic_object_list.addObject(cas_manager.symbolic_object.symbolicObject("sin(x)**2 +  cos(x)**2 + 2*sin(x)*cos(x)"))
#symbolic_object_list.addObject(cas_manager.symbolic_object.symbolicObject("x"))

#eatComputations.pendingComputations.put(("S-simplify", [1]))
#res = eatComputations.pendingResults.get()'''

#'''res = cas_manager.compute.compute("S-simplify", [1]).getComputableObject()
#cas_manager.compute.updateWithResult("S-simplify", [1], res)
#print(res)'''