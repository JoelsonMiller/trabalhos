#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

goal_x = 10.0

def callback(data):
	print("A pose em x = " + str(data.x) + " y = " + str(data.y) + " theta = " + str(data.theta))
	twist = Twist()

	twist.linear.x = (goal_x - data.x)
	if(math.fabs((goal_x - data.x)) < 0.1):
		twist.linear.x = 0.0

	pub.publish(twist)

def control_turtlesim():
	rospy.init_node("control", anonymous=True)
	rospy.Subscriber("/turtle1/pose", Pose, callback)
	rospy.spin()

if __name__ == "__main__":
	control_turtlesim()
