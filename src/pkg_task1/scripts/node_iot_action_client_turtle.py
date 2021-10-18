#!/usr/bin/env python

# ROS Node - Simple Action Client - Turtle

import rospy
import actionlib
import time
import requests

from pkg_ros_actions.msg import msgTurtleAction       # Message Class that is used by ROS Actions internally
from pkg_ros_actions.msg import msgTurtleGoal         # Message Class that is used for Goal messages

from pkg_iot_ros_bridge.msg import msgIotRosAction      # Message Class that is used by ROS Actions internally
from pkg_iot_ros_bridge.msg import msgIotRosGoal        # Message Class that is used for Goal Messages
from pkg_iot_ros_bridge.msg import msgIotRosResult      # Message Class that is used for Result Messages
from pkg_iot_ros_bridge.msg import msgMqttSub 

class SimpleActionClientTurtle:

    # Constructor
    def __init__(self):
        self._ac = actionlib.SimpleActionClient('/action_turtle',
                                                msgTurtleAction)
        self._as = actionlib.SimpleActionClient('/action_iot_ros',
                                                  msgIotRosAction)
        param_config_iot = rospy.get_param('config_iot')
        self._config_mqtt_pub_topic = param_config_iot['mqtt']['topic_pub']
        
        self._ac.wait_for_server()
        rospy.loginfo("Action server is up, we can send new goals!")

    # Function to send Goals to Action Servers
    def send_goal(self, arg_dis, arg_angle):
        
        # Create Goal message for Simple Action Server
        goal = msgTurtleGoal(distance=arg_dis, angle=arg_angle)
        
        '''
            * done_cb is set to the function pointer of the function which should be called once 
                the Goal is processed by the Simple Action Server.

            * feedback_cb is set to the function pointer of the function which should be called while
                the goal is being processed by the Simple Action Server.
        ''' 
        self._ac.send_goal(goal, done_cb=self.done_callback,
                           feedback_cb=self.feedback_callback)
        
        rospy.loginfo("Goal has been sent.")

    # Function print result on Goal completion
    def done_callback(self, status, result):
        rospy.loginfo("Status is : " + str(status))
        rospy.loginfo("Result is : " + str(result))
        res=list()
	res.append(result.final_x)
	res.append(result.final_y)
	res.append(result.final_theta)
        self.send_result(res)
        
   
    def send_result(self,arg_msg):
        goal_msg=msgIotRosGoal()
        goal_msg.protocol="mqtt"
        goal_msg.mode="pub"
        goal_msg.topic= self._config_mqtt_pub_topic 
        goal_msg.message=str(tuple(arg_msg))
        self._as.send_goal(goal_msg)
        parameters = {"id":"Sheet1", "turtle_x":arg_msg[0],"turtle_y":arg_msg[1],"turtle_theta":arg_msg[2]} 

	headers = {
        'Authorization': "Bearer [token]"
    	}
	URL = "https://script.google.com/macros/s/AKfycbzrUFi_nOO-9pNE88PNcOKtl2z9ki35SFWFv3dHPlNsVyUe0UxP/exec"  #need to change url

	r = requests.get(URL, params=parameters,headers=headers)

    # Function to print feedback while Goal is being processed
    def feedback_callback(self, feedback):
        rospy.loginfo(feedback)
	
        

def start(my_msg):
    if(my_msg.message == "start"):

        obj_client = SimpleActionClientTurtle()

    # send coordinates to trace hexagon
        obj_client.send_goal(2, 0)
        rospy.sleep(10)

        obj_client.send_goal(2, 60)
        rospy.sleep(10)

        obj_client.send_goal(2, 60)
        rospy.sleep(10)

        obj_client.send_goal(2, 60)
        rospy.sleep(10)
       
        obj_client.send_goal(2, 60)
        rospy.sleep(10)

        obj_client.send_goal(2, 60)
        rospy.sleep(10)

      

    # 4. Loop forever
   

# Main Function
def main():
    # 1. Initialize ROS Node
    rospy.init_node('node_simple_action_client_turtle')

    rospy.Subscriber("/ros_iot_bridge/mqtt/sub",msgMqttSub,start)
    rospy.spin()
    
if __name__ == '__main__':
    main()
