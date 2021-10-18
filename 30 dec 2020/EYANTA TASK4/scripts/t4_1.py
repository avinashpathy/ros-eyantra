#! /usr/bin/env python

import rospy
import sys
import copy

import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib

from pkg_task4.msg import msgFile
from hrwros_gazebo.msg import LogicalCameraImage
from pkg_vb_sim.srv import conveyorBeltPowerMsg
from hrwros_gazebo.msg import Model
from  pkg_vb_sim.srv import vacuumGripper

colour = []

class sort:

    # Constructor
    def __init__(self):
        rospy.init_node('node_t4_1', anonymous=True)
        rospy.Subscriber("/eyrc/vb/logical_camera_2",LogicalCameraImage,self.callback)
        self._robot_ns = '/' + 'ur5_2'
        self._planning_group = "ur5_2_planning_group"
        rospy.Subscriber("my_topic", msgFile, self.func_callback_topic_my_topic)  #subscribing to t4
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
        
        rospy.loginfo('\033[94m' + " >>> Init done." + '\033[0m')

    # Destructor
    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class CartesianPath Deleted." + '\033[0m')

    def callback(self,msg):
	#this is called everytime a message is detected by the subscriber
        try:
            if(msg.models[i].type!="ur5_2"):    
                if(((msg.models[i].pose.position.y)>-0.05) and ((msg.models[i].pose.position.y)<0.05)):
             		#called the constop function when the package is in the range
	            self.constop()
	            rospy.sleep(1)
		    self.act_vac()
                    self.bin_pose()
	            rospy.sleep(1)
	            self.constart()
        except:
    	    pass
    def func_callback_topic_my_topic(self,myMsg): 
	                                #t4 subscribed func
	print('######################################')
        rospy.loginfo("Data Received: (%s)", myMsg.col)
        colour.append(myMsg.col)
             
	     
    def bin_pose(self):
        #green bin
        lst_joint_angles_green = [1.667,-2.1484,-0.7726,-1.751,1.56,0.096]
        lst_joint_angles_up = [0,-2.383,-0.607,-1.721,1.61096,-1.57]
        
        #yellow bin predefined pose allZeros
        
        #red bin
        lst_joint_angels_red = [1.458306,-1.034272,1.1572377,-1.723733,-1.567390,3.0291449]

	self.set_joint_angles(lst_joint_angles_up)
	if(colour[0] == "green"):
	    colour.pop(0)
	    self.set_joint_angles(lst_joint_angles_green)
        if(colour[0] == "red"):
	    colour.pop(0)
	    self.set_joint_angles(lst_joint_angles_red)
        if(colour[0] == "yellow"):
	    colour.pop(0)
	    print(colour)
	    self.go_to_predefined_pose("allZeros")
	  
	self.dact_vac() 
	  

    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')
    

    
    def constart(self):
	#function to start conveyer belt
        conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
	conveyor_belt(90)

    def constop(self,number):
	#function to stop the conveyer belt
	conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
	conveyor_belt(0)
        
    def act_vac(self):
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vaccum_gripper(True)
    def dact_vac(self):
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vaccum_gripper(False)

           
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

def main():
    ur5_2 = sort()
    lst_joint_angles = [0,-2.3557,-0.986136,-1.3669,1.551589,1.56056] 

    while not rospy.is_shutdown():
        # 1. Go to Home Position
        ur5_2.set_joint_angles(lst_joint_angles)

    del ur5_2


if __name__ == '__main__':

    main()
