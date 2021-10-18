#! /usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
import rospkg
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

power_val = 90                                                            #stores the power value for the conveyor belt
                                                  
pack =dict()                                                              #dictionary that stores package name and colour

class pkg_sort:

    def __init__(self):
        rospy.init_node('node_t4', anonymous=True)
        rospy.Subscriber("/eyrc/vb/camera_1/image_raw",Image,self.callback)
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
    
  
        self.bridge = CvBridge()
        self.con_start(power_val)

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

                pack["package{}{}".format(i,j)] = colour                                   # pkg_colour with package name    
                
                
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
       conveyor_belt(power_val)

   
    def vacuum_griper(self,state):                                                       #function to activate and deactivate the vacuum gripper
         
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5/activate_vacuum_gripper/ur5_1",vacuumGripper)
        vaccum_gripper(state)
          
    def con_pose(self):                                                              #function that has coordinates to keep package near conveyor belt
   
        #convey_belt pose joint angles
        lst_joint_angles = [0,-2.399,-1.118,-1.1939,1.524,-1.572]   
        
        flag1 =  self.set_joint_angles(lst_joint_angles)
           
        if(flag1 == True):
            print("The ur5_1 has reached near conveyor belt")
           
            self.vacuum_griper(False)                                                #calling function to de-activate the vacuum gripper  
            
    def set_joint_angles(self, arg_list_joint_angles):

        list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo('\033[94m' + ">>> Current Joint Values:" + '\033[0m')
        rospy.loginfo(list_joint_values)

        self._group.set_joint_value_target(arg_list_joint_angles)
        self._group.plan()
        flag_plan = self._group.go(wait=True)

        list_joint_values = self._group.get_current_joint_values()
        rospy.loginfo('\033[94m' + ">>> Final Joint Values:" + '\033[0m')
        rospy.loginfo(list_joint_values)

        pose_values = self._group.get_current_pose().pose
        rospy.loginfo('\033[94m' + ">>> Final Pose:" + '\033[0m')
        rospy.loginfo(pose_values)

        if (flag_plan == True):
            rospy.loginfo(
                '\033[94m' + ">>> set_joint_angles() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> set_joint_angles() Failed." + '\033[0m')

        return flag_plan

    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')
    

def main():
    #First row
    lst_joint_angles_00 = [-0.267,-2.39,1.094,-1.856,-1.29,1.489]      #package00
    lst_joint_angles_00_0 = [-0.909,-1.204,0.14,-1.921,-2.1488,0.538]
    lst_joint_angles_00_1 =[-0.607,-1.415,0.361,-1.8763,-2.478,0.619]
    lst_joint_angles_00_2 =[-0.580,-1.144,-0.114,-2.059,1.266,-0.3669]
    
    lst_joint_angles_01 = [2.251,-1.5389,-0.588,-1.0716,0.8915,0]      #package01
    lst_joint_angles_01_1 = [2.615,-1.3736,-0.378,-1.381,-1.9714,-0.0569]
    
    lst_joint_angles_02 = [1.0571,-1.8535,-0.2083,-1.0797,2.0845,0.0962]      #package02
    lst_joint_angles_02_0 = [0.616,-1.5909,-0.555,-0.9954,2.5255,0.0961]

    #second row
    lst_joint_angles_10 = [-0.849887,-1.43650,0.828597,0.607385,2.274718,-0.000851]            #package10
    lst_joint_angles_10_0 = [-0.58680,-1.57314,0.977149,0.595126,2.537753,-0.00103]

    lst_joint_angles_11 = [-2.01037,-1.889515,1.1925625,0.6969144,1.067172,-1.5003408]          #package11
    lst_joint_angles_11_0 = [-2.85409,-2.166812,1.28145,0.885655,0.223412,-1.500694]

    lst_joint_angles_12 = [1.016763,-1.508867,-1.022580,2.588313,-2.0607623,-1.5959657]         #package12
    lst_joint_angles_12_0 = [0.691132,-1.329716,-1.18804027,2.59096478,-2.38589749,-1.569518]

   
    #third row
    lst_joint_angles_20 = [-0.8969,-1.6420,1.9698,2.8133,-2.245,0.0969]      #package20
    lst_joint_angles_20_0 = [-0.6064,-1.7692,2.0942,2.8158,-2.5352,0.09676]
    lst_joint_angles_20_1 =[-0.6064,-1.7204,2.0492,2.599,-1.5134,-0.013]
    
    lst_joint_angles_22 = [0.96,-1.4543,-2.0611,0.3755,2.1740,0]             #package22
    lst_joint_angles_22_0 = [0.626,-1.2921,-2.187,0.3398,2.5152,0.001]
    lst_joint_angles_22_1 = [0.626,-1.2921,-2.187,0.3376,0.9422,0.001]
   
    #fourth row
    lst_joint_angles_32 = [0.9882,-1.516,-2.131,-2.656,-2.356,0.005]      #package32
    lst_joint_angles_32_0 = [0.7057,-1.3916,-2.2327,-2.687,-2.518,-0.005]
    lst_joint_angles_32_1 = [0.7057,-1.3899,-2.2341,-2.68,-0.877,-0.005]  
     

    package = pkg_sort()
    rospy.sleep(1)
    #1
    try:
        package.set_joint_angles(lst_joint_angles_02)
        rospy.sleep(1)
        package.vacuum_griper(True)              #activating vaccum gripper 
        rospy.sleep(1)                                        
        package.set_joint_angles(lst_joint_angles_02_0) 
        rospy.sleep(2)
    
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)
    #2
    try:
        package.set_joint_angles(lst_joint_angles_01)
        rospy.sleep(2)
        package.vacuum_griper(True)                  #activating vaccum gripper                                         
        rospy.sleep(2)
        package.set_joint_angles(lst_joint_angles_01_1)
        rospy.sleep(2)
        

        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)
        
    
    #3
    try:
        package.set_joint_angles(lst_joint_angles_00)
        rospy.sleep(2)
        package.set_joint_angles(lst_joint_angles_00_0) 
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)                                            
        package.set_joint_angles(lst_joint_angles_00_1) 
        rospy.sleep(2) 
        package.set_joint_angles(lst_joint_angles_00_2) 
        rospy.sleep(2) 
       
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)

    #4
    try:
        package.set_joint_angles(lst_joint_angles_12)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)    
        package.set_joint_angles(lst_joint_angles_12_0)
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)

    #5'
    try:
        package.set_joint_angles(lst_joint_angles_11)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)    
        package.set_joint_angles(lst_joint_angles_11_0)
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)

    #6
    try:
        package.set_joint_angles(lst_joint_angles_10)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)    
        package.set_joint_angles(lst_joint_angles_10_0)
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)

        
    #7
    try:
        package.set_joint_angles(lst_joint_angles_20)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)                                            #activating vaccum gripper 
        package.set_joint_angles(lst_joint_angles_20_0) 
        rospy.sleep(2)    
        package.set_joint_angles(lst_joint_angles_20_1) 
        rospy.sleep(2)
       
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)
    
    #8 
    try:
        package.set_joint_angles(lst_joint_angles_22)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)                                             #activating vaccum gripper 
        package.set_joint_angles(lst_joint_angles_22_0) 
        rospy.sleep(2) 
        package.set_joint_angles(lst_joint_angles_22_1) 
        rospy.sleep(2) 
        
        
        package.con_pose()
        rospy.sleep(2) 
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)
    
    #9
    try:
        package.set_joint_angles(lst_joint_angles_32)
        rospy.sleep(1)
        package.vacuum_griper(True)                  #activating vaccum gripper 
        rospy.sleep(1)                                           #activating vaccum gripper 
        
        package.set_joint_angles(lst_joint_angles_32_0) 
        rospy.sleep(2) 
        package.set_joint_angles(lst_joint_angles_32_1) 
        rospy.sleep(2) 
        
        package.con_pose()
        rospy.sleep(2)
    except:
        package.vacuum_griper(False)
        package.go_to_predefined_pose(allZeros)
        

    del package  

if __name__ == '__main__':

    main()
    rospy.time()
