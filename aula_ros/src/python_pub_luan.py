#!/usr/bin/env python

import rospy
from std_msgs.msg import ColorRGBA

def pub_test():

	rospy.init_node("node_pub_luan", anonymous = True);
	pub = rospy.Publisher("topic_pub_luan",ColorRGBA, queue_size=10);
	taxa_pub = rospy.Rate(10);

	while not rospy.is_shutdown():
		cor = ColorRGBA();
		cor.r = 255;
		cor.g = 255;
		cor.b = 255;
		cor.a = 0;
		pub.publish(cor);	
		taxa_pub.sleep();

if __name__=='__main__':
	try:
		pub_test();
	except rospy.ROSInterruptException:
		pass
		
