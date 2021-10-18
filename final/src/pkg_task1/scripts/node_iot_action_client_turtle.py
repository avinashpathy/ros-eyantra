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

hex_side=2                                            #define side length of hexagon
hex_angle=60                                          #define angle measure of hexagon

sheet_url="https://script.google.com/macros/s/AKfycbx3rCuGURQoimBmK2uWZt4WZkPkbV0wmpfBo2YMAlefQTT7Zfh_/exec"               #url for the google sheet
sheet_url_eyantra =  "https://script.google.com/macros/s/AKfycbw850dk4moVgebU2GGe0PUQUvvg8jTpSjBQCawJt3_13vgujLk/exec"     #url for eyantra google sheet

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
        res=list()                                      #storing coordinates in list
	res.append(result.final_x)
	res.append(result.final_y)
	res.append(result.final_theta)
        self.send_result(res)                    
        self.send_to_sheet(res) 
	self.send_to_sheet_eyantra(res)
                  
    #function to push data to spread sheet 
    def send_to_sheet(self,arg_msg):
        parameters = {"id":"task1", "turtle_x":arg_msg[0],"turtle_y":arg_msg[1],"turtle_theta":arg_msg[hex_side]} 

	headers = {
        'Authorization': "Bearer [token]"
    	}
	URL = sheet_url
	response = requests.get(URL, params=parameters,headers=headers)
	print(response.content)

   
    #function to push data to eyantra_spreadsheet
    def send_to_sheet_eyantra(self,arg_msg):
        parameters = {"id":"task1","team_id":865,"unique_id":"aBCaRvEc", "turtle_x":arg_msg[0],"turtle_y":arg_msg[1],"turtle_theta":arg_msg[hex_side]} 
	

	headers = {
        'Authorization': "Bearer [token]"
    	}
	URL = sheet_url_eyantra
	r = requests.get(URL, params=parameters,headers=headers)

     #function to push gata to hivemq
    def send_result(self,arg_msg):
        goal_msg=msgIotRosGoal()
        goal_msg.protocol="mqtt"
        goal_msg.mode="pub"
        goal_msg.topic= self._config_mqtt_pub_topic 
        goal_msg.message=str(tuple(arg_msg))
        self._as.send_goal(goal_msg)
        

    # Function to print feedback while Goal is being processed
    def feedback_callback(self, feedback):
        rospy.loginfo(feedback)
	
        
#function to start sending code to simpleAction Server 
def start(my_msg):
    if(my_msg.message == "start"):                       #if input message from mqtt is start the the client start sending goal

        obj_client = SimpleActionClientTurtle()

    # send coordinates to trace hexagon
        for i in range(6):
            if(i==0):

                obj_client.send_goal(hex_side, 0)
                rospy.sleep(10)
            else:
                obj_client.send_goal(hex_side, hex_angle)
                rospy.sleep(15)  

# Main Function
def main():
    # 1. Initialize ROS Node
    rospy.init_node('node_iot_action_client_turtle')

    rospy.Subscriber("/ros_iot_bridge/mqtt/sub",msgMqttSub,start)
     # 4. Loop forever
    rospy.spin()
    
if __name__ == '__main__':
    main()
