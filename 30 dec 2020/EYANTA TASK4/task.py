#! /usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
import rospkg

import yaml
import os
import math
import time
import sys
import copy



from pkg_vb_sim.srv import conveyorBeltPowerMsg
from hrwros_gazebo.msg import Model
from  pkg_vb_sim.srv import vacuumGripper
from moveit_commander import MoveGroupCommander, roscpp_initialize
import cv2

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import numpy as np
from pyzbar.pyzbar import decode

box_length = 0.15                                   # Length of the Package
vacuum_gripper_width = 0.115                        # Vacuum Gripper Width  
pkg_no = 9                                            #number of packages need to be sorted
pose_x = 0.28                                        #reference coordinates 
pose_y = 6.59
pose_z = 1.92
 
power_val = 30                                                            #stores the power value for the conveyor belt
                                                  
pack =dict()
class pkg_sort:

    def __init__(self):
        rospy.init_node('node_t4', anonymous=True)
        rospy.Subscriber("/eyrc/vb/camera_1/image_raw",Image,self.callback)
       
        self.bridge = CvBridge()
        self.con_start(power_val)
        rospy.loginfo('\033[94m' + " >>> Init done." + '\033[0m')
       # self.pack = dict()
    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        (rows,cols,channels) = cv_image.shape
    
        image = cv_image
      
       
        for i in range (4):                                                                 #package in different row and column number is recognised using cropping technique

            for j in range (3):
                
                image =cv_image[(300+i*150):(450+i*150),(110+j*190):(250+j*190)]
                
                colour = self.pkg_color(image)

                pack["package{}{}".format(i,j)] = colour,i,j                               # pkg_colour,row_no,column_no stored in pack dictionary 
                                   
            rospy.sleep(1)
    
        cv2.waitKey(3)

    def pkg_color(self,arg_img):
        qr_result = decode(arg_img)

        if ( len( qr_result ) > 0):
    
            return (qr_result[0].data)
        
        else :
            return ('NA')

    def con_start(self,value):                                                           #powers the conveyor belt
       
       conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
       conveyor_belt(value)

class ur5 (pkg_sort):

    def __init__(self):

        self._robot_ns = '/' + 'ur5_1'
        self._planning_group = "ur5_1_planning_group"
        
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander(robot_description= self._robot_ns + "/robot_description", ns=self._robot_ns)
        self._scene = moveit_commander.PlanningSceneInterface(ns=self._robot_ns)
        self._group = moveit_commander.MoveGroupCommander(self._planning_group, robot_description= self._robot_ns + "/robot_description", ns=self._robot_ns)
        self._display_trajectory_publisher = rospy.Publisher( self._robot_ns + '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)
        self._exectute_trajectory_client = actionlib.SimpleActionClient( self._robot_ns + '/execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()

        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()
        rospy.loginfo('\033[94m' + " >>> Init done." + '\033[0m')
	
  
    def pos(self,i):

        row_no=pack.values()[i][1]                                                             #first element stores the row number      
       
        col_no=pack.values()[i][2]                                                             #second element stores the column number
        
        ur5_1_pose=geometry_msgs.msg.Pose()
       
        ur5_1_pose.position.x = pose_x - col_no*0.28                                  #getting the x y z coordiante  from a std referenence box ie first row and first column pkg since shelf is fixed
     
        ur5_1_pose.position.y = pose_y - vacuum_gripper_width - (box_length/2)
    
        ur5_1_pose.position.z = pose_z - row_no*0.24 
   
        ur5_1_pose.orientation.x = 0
        ur5_1_pose.orientation.y = 0
        ur5_1_pose.orientation.z = 0
        ur5_1_pose.orientation.w = 0
        print ("THE GIVEN DESTINATION IS",ur5_1_pose)
       
        flag = self.go_to_pose(ur5_1_pose)
   
    
        
        if(flag == True): 
            print("The ur5_1 has reached near shelf")

            self.vacuum_griper(True)  
    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')                                                  #calling function to activate the vacuum gripper  

    def vacuum_griper(self,state):                                                       #function to activate and deactivate the vacuum gripper
         
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5/activate_vacuum_gripper_ur5_1",vacuumGripper)
        vaccum_gripper(state)
          
    def con_pose(self):                                                              #function that has coordinates to keep package near conveyor belt
   
        ur5_1_home_pose = geometry_msgs.msg.Pose()                  
            
        ur5_1_home_pose.position.x = -0.8 
        ur5_1_home_pose.position.y = 7
        ur5_1_home_pose.position.z = 1 + vacuum_gripper_width + (box_length/2)
            
         # This to keep EE parallel to Ground Plane
            
        ur5_1_home_pose.orientation.x = -0.5
        ur5_1_home_pose.orientation.y = -0.5                               
        ur5_1_home_pose.orientation.z = 0.5
        ur5_1_home_pose.orientation.w = 0.5
        flag1 = self.go_to_pose(ur5_1_home_pose)
    
        
        
        if(flag1 == True):
            print("The ur5_1 has reached near conveyor belt")
           
            self.vacuum_gripper(False)                          #calling function to de-activate the vacuum gripper  
            
     

    def go_to_pose(self,arg_pose):
        os
        
        pose_values = self._group.get_current_pose().pose
        
        rospy.loginfo('\033[94m' + ">>> Current Pose:" + '\033[0m')
        rospy.loginfo(pose_values)

        self._group.set_pose_target(arg_pose)
        flag_plan = self._group.go(wait=True)  # wait=False for Async Move

        pose_values = self._group.get_current_pose().pose
        rospy.loginfo('\033[94m' + ">>> Final Pose:" + '\033[0m')
        rospy.loginfo(pose_values)

        list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo('\033[94m' + ">>> Final Joint Values:" + '\033[0m')
        rospy.loginfo(list_joint_values)

        if (flag_plan == True):
            rospy.loginfo('\033[94m' + ">>> go_to_pose() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> go_to_pose() Failed. Solution for Pose not Found." + '\033[0m')

        return flag_plan


def main():
    i=0
    #print("The value",sys.argv[0])
    package = pkg_sort()
    ur5_1_arm = ur5()
    pkg_no=9
    while not rospy.is_shutdown():                                        #runs until the ros has been called for shutdown
        while (pkg_no != 0): 
            
            ur5_1_arm.go_to_predefined_pose("straightUp")                                             #checks for whether all packages have been fetched
            ur5_1_arm.pos(i)
            i+=1                                                   #the ur5_1 goes to the required package position
            print ('The package has been fetched')
            rospy.sleep(0.1)
                                                          #the ur5_1 goes near the conveyor belt position and drops the package
            ptint ('Package has been placed on the conveyor belt')
            pkg_no -= 1 
    
    del package  

if __name__ == '__main__':

    main()
    rospy.time()
