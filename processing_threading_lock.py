import multiprocessing
import time
import threading

start = time.perf_counter()

def counter_one(counter_x, aux):
	while(1):
		aux.value = int(input("Type the number of counter or -1 to finished: "))
		if(aux.value > 0):
			for i in range(aux.value):
				counter_x.value += 1
				time.sleep(0.01)
			print ("The counter final's value is: " + str(counter_x.value))
			counter_x.value = 0
			aux.value = 0
		elif(aux.value < 0):
			break

def counter_two(aux_x, aux):
	while(1):
		if(aux.value > 0 and aux_x.value != 0):
			time.sleep(0.5)
			print("\nThe counter's num is: " + str(aux_x.value) + " til " + str(aux.value))
		elif(aux.value < 0):
			break

x = multiprocessing.Value('i', 0)
y = multiprocessing.Value('i', 0)
aux = multiprocessing.Value('i', 0)

process_one = threading.Thread(target=counter_one, args = (x, aux) )
process_two = multiprocessing.Process(target=counter_two, args = (x, aux) )

process_one.start()
process_two.start()

process_one.join()
process_two.join()

finish = time.perf_counter()

print("Finished in "+str(round(finish - start, 2))+" seconds")

