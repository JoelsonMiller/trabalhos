#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

goal_x = 3.0
goal_y = 2.0

def callback(data):

	print("A pose em x = " + str(data.x) + " y = " + str(data.y) + " theta = " + str(data.theta))
	twist = Twist()

	twist.linear.x = math.hypot((goal_x - data.x),(goal_y-data.y))/2
	goal_orientation = math.atan2(goal_y - data.y, goal_x - data.x) #returns the quadrant angle in radians
	twist.angular.z = (goal_orientation - data.theta)*4

	if(math.fabs((goal_x - data.x)) < 0.05 and math.fabs(goal_y - data.y) < 0.05):
		twist.linear.x = 0.0
		twist.angular.z = 0.0

	pub.publish(twist)

def control_turtlesim():
	rospy.init_node("control", anonymous=True)
	rospy.Subscriber("/turtle1/pose", Pose, callback)
	rospy.spin()

if __name__ == "__main__":
	control_turtlesim()
