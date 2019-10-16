#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def callback_function (mensagem):
	print mensagem.data;

rospy.init_node("vreu");
subs = rospy.Subscriber("info", Float32, callback_function);

rospy.spin() #Mantem o programa ativo para receber mensagens. IMPORTANTE!!!
