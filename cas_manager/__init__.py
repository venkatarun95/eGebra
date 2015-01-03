'''import symbolic_object
from symbolic_object_list import symbolic_object_list
import compute
import scheduler
import cas_manager_interface'''

#import server
import cas_manager_interface
import scheduler
#Call the various initializers
#symbolic_object_list.initialize()

eatComputations = scheduler.scheduler()
cas_manager_interface.initialize(eatComputations)

#while True:
try:
	eatComputations.start()
except:
	print("Exception detected in the scheduler. Researting it, all computation requests will be lost.")
	#Warning: Exceptions in the thread do not reach here. Do something else to resolve this issue
		#eatComputations.pause()

def computationScheduler():
	return eatComputations
