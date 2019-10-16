#!/usr/bin/env python

import rospy
import primitivas as p
from std_msgs.msg import Char

def function_callback(data):
	p.leds(data.data)

def function():
	rospy.init_node("leds_se", anonymous=True)
	rospy.Subscriber("leds", Char, function_callback)
	rospy.spin()	

if __name__=='__main__':
	try:
		function()	
	except rospy.ROSInterruptException:
		pass
