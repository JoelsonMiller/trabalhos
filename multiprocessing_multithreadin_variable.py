import multiprocessing
import time
import threading

start = time.perf_counter()

def counter_one(counter_x):
	ans = int(input("Type the number of counter: "))
	for i in range(ans):
		counter_x.value += 1

def counter_two(counter_y):
	for i in range(10000000):
		counter_y.value += 1

x = multiprocessing.Value('i', 0)
y = multiprocessing.Value('i', 0)

process_one = threading.Thread(target=counter_one, args = (x, ) )
process_two = multiprocessing.Process(target=counter_two, args = (y,) )

process_one.start()
process_two.start()

process_one.join()
process_two.join()

finish = time.perf_counter()

print("Finished in "+str(round(finish - start, 2))+" seconds")
print ("The counter final's value is: " + str(x.value))
print ("The counter final's value is: " + str(y.value))

