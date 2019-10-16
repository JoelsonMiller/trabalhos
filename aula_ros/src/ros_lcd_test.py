#!/usr/bin/env python

import rospy
import primitivas as p
from std_msgs.msg import String

def function_callback(string):
#	lcd_init()
	p.lcd_escrever(string.data)

def function():
	rospy.init_node("lcd_node", anonymous=True)
	rospy.Subscriber("lcd_write", String, function_callback)
	rospy.spin()

if __name__=='__main__':
	try:
		function()
	except rospy.ROSInterruptException:
		pass
