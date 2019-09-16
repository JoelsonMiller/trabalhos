#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

from package.srv import PoseGoal, PoseGoalResponse

pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

goal_x = 0
goal_y = 0
goal_theta = 0

def callback(data):
	global pose_x
	global pose_y
	global pose_theta

	pose_x = data.x
	pose_y = data.y
	pose_theta = data.theta

def go_to_goal(srv):


	global pose_x
	global pose_y
	global pose_theta
	#pose_x = pose_x_aux
	#pose_y = pose_x_aux
	#pose_theta = pose_theta_aux

	twist=Twist()
	print("The objective is: x = "+str(srv.goal_x)+" y = "+str(srv.goal_y))
	print("A pose em x = " + str(pose_x) + " y = " + str(pose_y) + " theta = " + str(pose_theta))

	while(math.fabs((srv.goal_x - pose_x)) > 0.05 and math.fabs(srv.goal_y -  pose_y) > 0.05):
		print("A pose em x = " + str(pose_x) + " y = " + str(pose_y) + " theta = " + str(pose_theta))
		twist.linear.x = math.hypot((srv.goal_x - pose_x),(srv.goal_y-pose_y))/2
		goal_orientation = math.atan2(srv.goal_y - pose_y, srv.goal_x - pose_x) #returns the quadrant angle in radians
		twist.angular.z = (goal_orientation - pose_theta)*4
		pub.publish(twist)

	twist.linear.x = 0.0
	twist.angular.z = 0.0

	pub.publish(twist)
	return PoseGoalResponse()

def control_turtlesim():
	rospy.init_node("control", anonymous=True)
	rospy.Subscriber("/turtle1/pose", Pose, callback)
	s = rospy.Service("/pose_goal", PoseGoal, go_to_goal)
	rospy.spin()

if __name__ == "__main__":
	control_turtlesim()
