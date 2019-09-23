import multiprocessing
import time

x = 0
y = 0

start = time.perf_counter()

def counter_one():
	global x
	for i in range(500000000):
		x = x + 1

def counter_two():
	global y
	for i in range(500000000):
		y = y + 1

process_one = multiprocessing.Process(target=counter_one)
process_two = multiprocessing.Process(target=counter_two)

process_one.start()
process_two.start()

process_one.join()
process_two.join()

#counter_one()
#counter_two()

finish = time.perf_counter()

print("Finished in "+str(round(finish - start, 2))+" seconds")

