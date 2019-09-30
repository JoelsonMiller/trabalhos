import multiprocessing
import time

x = multiprocessing.Value('i', 0)

start = time.perf_counter()

def counter_one(counter_x):
	for i in range(1000000):
		with counter_x.get_lock():
			counter_x.value += 1

def counter_two(counter_x):
	for i in range(1000000):
		with counter_x.get_lock():
			counter_x.value += 1

process_one = multiprocessing.Process(target=counter_one, args = (x,) )
process_two = multiprocessing.Process(target=counter_two, args = (x,) )

process_one.start()
process_two.start()

process_one.join()
process_two.join()

#counter_one()
#counter_two()

finish = time.perf_counter()

print("Finished in "+str(round(finish - start, 2))+" seconds")
print ("The counter final's value is: " + str(x.value))
#print ("The counter final's value is: " + str(y.value))
