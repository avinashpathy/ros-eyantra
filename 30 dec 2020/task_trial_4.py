#! /usr/bin/env python

import rospy
import sys
import copy
import cv2
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pkg_vb_sim.srv import conveyorBeltPowerMsg
from  pkg_vb_sim.srv import vacuumGripper
import numpy as np
from pyzbar.pyzbar import decode

box_length = 0.15                                   # Length of the Package
vacuum_gripper_width = 0.115                        # Vacuum Gripper Width  
pkg_no = 9                                          #number of packages need to be sorted
pose_x = 0.28                                        #reference coordinates 
pose_y = 6.59
pose_z = 1.92

value = 30                                          #defining the power of the conveyor belt 
pack = {}                                           
class pkg_sort:
    def __init__(self):
        
        self._planning_group = "ur5_1_planning_group"
        self._commander = moveit_commander.roscpp_initialize(sys.argv)
        self._robot = moveit_commander.RobotCommander()
        self._scene = moveit_commander.PlanningSceneInterface()
        self._group = moveit_commander.MoveGroupCommander(self._planning_group)
        self._display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=1)

        self._exectute_trajectory_client = actionlib.SimpleActionClient(
            'execute_trajectory', moveit_msgs.msg.ExecuteTrajectoryAction)
        self._exectute_trajectory_client.wait_for_server()
        self._planning_frame = self._group.get_planning_frame()
        self._eef_link = self._group.get_end_effector_link()
        self._group_names = self._robot.get_group_names()

        self.bridge = CvBridge()


        self.con_start(value)                                                          #powers the conveyor belt
   
     
       
       
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
        
       # return pack 
  

  
    def pkg_color(self,arg_img):
        qr_result = decode(arg_img)

        if ( len( qr_result ) > 0):
    
            return (qr_result[0].data)
        
        else :
            return ('NA')

    def pos(self):
        #row_col = []                                                                  #list that stores row and column number
        for i in range (pkg_no):
  
         #   row_col.append(pack.keys())                                                           #storing the row and coln number in the row_col list

            row_no=0#pack.values()[i][0]                                                             #first element stores the row number      
       
            col_no=1#pack.values()[i][1]                                                             #second element stores the column number
        
            ur5_2_pose=geometry_msgs.msg.Pose()
        
            ur5_2_pose.position.x = pose_x - col_no*0.28                                  #getting the x y z coordiante  from a std referenence box ie first row and first column pkg since shelf is fixed
     
            ur5_2_pose.position.y = pose_y - vacuum_gripper_width - (box_length/2)
    
            ur5_2_pose.position.z = pose_z - row_no*0.24 
   
            ur5_2_pose.orientation.x = 0
            ur5_2_pose.orientation.y = 0
            ur5_2_pose.orientation.z = 0
            ur5_2_pose.orientation.w = 0
            flag = self.go_to_pose(ur5_2_pose)
   
            print("The ur5_2 has reached near shelf")
        
            if(flag == True): 

                self.vacuum_gripper(True)                                                    #calling function to activate the vacuum gripper  
   
                self.con_pose() 
    def vacuum_griper(self,state):                                                       #function to activate and deactivate the vacuum gripper
         
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vaccum_gripper(state)
     
    def con_start(self,value):                                                           #powers the conveyor belt

	conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
	conveyor_belt(value)
          
    def con_pose(self):                                                              #function that has coordinates to keep package near conveyor belt
   
        ur5_2_home_pose = geometry_msgs.msg.Pose()                  
            
        ur5_2_home_pose.position.x = -0.8 
        ur5_2_home_pose.position.y = 7
        ur5_2_home_pose.position.z = 1 + vacuum_gripper_width + (box_length/2)
            
         # This to keep EE parallel to Ground Plane
            
        ur5_2_home_pose.orientation = [-0.5,-0.5,0.5,0.5]

        flag1 = self.go_to_pose(ur5_2_home_pose)
    
        print("The ur5_2 has reached near conveyor belt")
        
        if(flag1 == True):

            self.vacuum_gripper(False)   						#calling function to de-activate the vacuum gripper  
    	    
	 

    def go_to_pose(self,arg_pose):
        
	
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
  
   
    rospy.init_node('node_t4', anonymous=True)                        #initialise the node
    

    
    pkge = pkg_sort() 
    
    #package = dict()
    rospy.Subscriber("/eyrc/vb/camera_1/image_raw", Image,pkge.callback)  

    pkge.pos()
if __name__ == '__main__':

    main()
    

     

     
 
        
  
    
