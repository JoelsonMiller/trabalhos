#!/usr/bin/env python
import rospy
import primitivas as p
from std_msgs.msg import Float32

def function():

	rospy.init_node("pot_ros", anonymous=True)
	pub = rospy.Publisher("pot", Float32, queue_size=10)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		pot_value = Float32()
		pot_value.data = p.lepot(0)
		pub.publish(pot_value)
		rate.sleep()

if __name__=="__main__":
	try:
		function()	
	except rospy.ROSInterruptException:
		pass
