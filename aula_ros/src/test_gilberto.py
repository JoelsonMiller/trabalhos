#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
#HCSR04 imports
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def pub_test():
	#Inicio do programa
	rospy.init_node("pub_gilberto", anonymous = True)
	pub = rospy.Publisher("pub_gilberto_topic", Float32, queue_size = 10)
	taxa_pub = rospy.Rate(10)
	
	while not rospy.is_shutdown():
		dist = Float32()
		dist.data = distance()
		pub.publish(dist) 
		taxa_pub.sleep()

if __name__ == '__main__':
	try:
		pub_test()
	except rospy.ROSInterruptException:
		pass
