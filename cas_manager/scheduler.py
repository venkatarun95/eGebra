import Queue
import threading

import cas_manager.compute

class scheduler(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.pendingComputations = Queue.PriorityQueue() #Format: (priority, keyStr, objKeys) where objKeys are the objects over which computation is to be applied and keyStr specifies the type of computation
		self.pendingResults = Queue.Queue() #queue from which the results can be picked

	def scheduleComputation(self, keyStr, objKeys, priority = 0):
		self.pendingComputations.put((priority, keyStr, objKeys))

	def run(self, ):
		while True:
			task = self.pendingComputations.get()
			try:
				res = cas_manager.compute.compute(task[1], task[2])
			except:
				print("Exception encountered in executing task ("+task+"). Skipping it.")
				self.pendingResults.put((task, []))
			#print "scheduler.py:scheduler:run :- Result of computation:- "
			#print res
			self.pendingResults.put((task, res))
			self.pendingComputations.task_done()