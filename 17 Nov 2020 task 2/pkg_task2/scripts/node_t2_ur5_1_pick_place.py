#! /usr/bin/env python



from __future__ import print_function
from six.moves import input

import rospy
import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
import math
import pkg_vb_sim

#import sys
#import copy
#import rospy
#import moveit_commander
#import moveit_msgs.msg
#import geometry_msgs.msg
#from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from  pkg_vb_sim.srv import vacuumGripper

class Ur5Moveit:

    # Constructor
    def __init__(self):

        rospy.init_node('node_eg3_set_joint_angles', anonymous=True)
	
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
	self.box_name = ''

        rospy.loginfo(
            '\033[94m' + "Planning Group: {}".format(self._planning_frame) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "End Effector Link: {}".format(self._eef_link) + '\033[0m')
        rospy.loginfo(
            '\033[94m' + "Group Names: {}".format(self._group_names) + '\033[0m')

        rospy.loginfo('\033[94m' + " >>> Ur5Moveit init done." + '\033[0m')

    def go_to_pose(self, arg_pose):

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
            rospy.loginfo(
                '\033[94m' + ">>> go_to_pose() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> go_to_pose() Failed. Solution for Pose not Found." + '\033[0m')

        return flag_plan


    def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
	
	box_name = self.box_name
	scene = self._scene

	
	start = rospy.get_time()
	seconds = rospy.get_time()
	while (seconds - start < timeout) and not rospy.is_shutdown():
	# Test if the box is in attached objects
	    attached_objects = scene.get_attached_objects([box_name])
	    is_attached = len(attached_objects.keys()) > 0

	# Test if the box is in the scene.
	# Note that attaching the box will remove it from known_objects
	    is_known = box_name in scene.get_known_object_names()

	# Test if we are in the expected state
	    if (box_is_attached == is_attached) and (box_is_known == is_known):
	        return True

	# Sleep so that we give other threads time on the processor
	    rospy.sleep(0.1)
	    seconds = rospy.get_time()

	# If we exited the while loop without returning then we timed out
        return False
    def add_box(self, timeout=4):
	# Copy class variables to local variables to make the web tutorials more clear.
	# In practice, you should use the class variables directly unless you have a good
	# reason not to.
	box_name = self.box_name
	scene = self._scene

	## BEGIN_SUB_TUTORIAL add_box
	##
	## Adding Objects to the Planning Scene
	## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	## First, we will create a box in the planning scene between the fingers:
	box_pose = geometry_msgs.msg.PoseStamped()
	box_pose.header.frame_id = "world"
	#box_pose.pose.orientation.x = 0.043213
	##box_pose.pose.orientation.y = 0.024761
	#sbox_pose.pose.orientation.z = -0.019710
	box_pose.pose.orientation.w = 1
	box_pose.pose.position.x = 0.038314
	box_pose.pose.position.y = 0.453061
	box_pose.pose.position.z = 1.865431 # above the panda_hand frame
	box_name = "box"
	scene.add_box(box_name, box_pose, size=(0.15, 0.15, 0.15))

	## END_SUB_TUTORIAL
	# Copy local variables back to class variables. In practice, you should use the class
	# variables directly unless you have a good reason not to.
	self.box_name=box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)
    def call_func(self):
	return "true"

    def attach_box(self, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
	box_name = self.box_name
	robot = self._robot
	scene = self._scene
	eef_link = self._eef_link
	group_names = self._group_names

    ## BEGIN_SUB_TUTORIAL attach_object
    ##
    ## Attaching Objects to the Robot
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ## Next, we will attach the box to the Panda wrist. Manipulating objects requires the
    ## robot be able to touch them without the planning scene reporting the contact as a
    ## collision. By adding link names to the ``touch_links`` array, we are telling the
    ## planning scene to ignore collisions between those links and the box. For the Panda
    ## robot, we set ``grasping_group = 'hand'``. If you are using a different robot,
    ## you should change this value to the name of your end effector group name.
	grasping_group = 'ur5_1_planning_group'
	touch_links = robot.get_link_names(group=grasping_group)
        
        #return activate_vacuum_gripper
	#result = activate_vacuum_gripper(True)

       # rosservice call /eyrc/vb/ur5_1/activate_vacuum_gripper "activate_vacuum_gripper: true"

	scene.attach_box(eef_link, box_name, touch_links=touch_links)
	#return result
	## END_SUB_TUTORIAL
    

    
    def go_to_predefined_pose(self, arg_pose_name):
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')
   
    
    # Destructor
    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Ur5Moveit Deleted." + '\033[0m')


def main():

    ur5 = Ur5Moveit()
    ur5.add_box()
    #ur5_pose_1 = geometry_msgs.msg.Pose()
    #ur5_pose_1.position.x = -0.817261772949
    #ur5_pose_1.position.y = -0.109110076352
    #ur5_pose_1.position.z = 0.94446979642
    #ur5_pose_1.orientation.x = -0.999999995957
    #ur5_pose_1.orientation.y = 4.37354574363e-05
    #ur5_pose_1.orientation.z = 7.85715579538e-05
    #ur5_pose_1.orientation.w = 2.12177767514e-09

    #ur5_pose_2 = geometry_msgs.msg.Pose()
    #ur5_pose_2.position.x = 0.190686
    #ur5_pose_2.position.y = 0.802108
    #ur5_pose_2.position.z = 0.802108
    # ur5_pose_2.orientation.x = -0.199396929724
    # ur5_pose_2.orientation.y = 1.64394297608e-05
    # ur5_pose_2.orientation.z = 0.979918803013
    # ur5_pose_2.orientation.w = 6.03911583936e-05

    ur5_pose_3 = geometry_msgs.msg.Pose()
    ur5_pose_3.position.x = 0.033298
    ur5_pose_3.position.y = 0.250411
    ur5_pose_3.position.z = 1.911618
    ur5_pose_3.orientation.x = 0.935613875737
    ur5_pose_3.orientation.y = 0.97190802743
    ur5_pose_3.orientation.z = -0.00833308772292
    ur5_pose_3.orientation.w = -0.0121472162087

    ur5_pose_5 = geometry_msgs.msg.Pose()
    ur5_pose_5.position.x = 0.050234
    ur5_pose_5.position.y = -0.125477
    ur5_pose_5.position.z = 1.912
    ur5_pose_5.orientation.x = 0.935613875737
    ur5_pose_5.orientation.y = 0.97190802743
    ur5_pose_5.orientation.z = -0.00833308772292
    ur5_pose_5.orientation.w = -0.0121472162087

    #ur5_pose_4 = geometry_msgs.msg.Pose()
    #ur5_pose_4.position.x =1.2
    #ur5_pose_4.position.y = -0.8
    #ur5_pose_4.position.z = 1
    #ur5_pose_4.orientation.x = -(math.pi)/2
    #ur5_pose_4.orientation.y = -(math.pi)/2
    #ur5_pose_4.orientation.z = 0
   

    ur5_pose_4 = geometry_msgs.msg.Pose()
    ur5_pose_4.position.x = -0.57560
    ur5_pose_4.position.y = -0.348486
    ur5_pose_4.position.z = 1.464110
   #ur5_pose_4.orientation.x = 3.110217
    #ur5_pose_4.orientation.y = 0.089779
    #ur5_pose_4.orientation.z = -1.393278

    #ur5_pose_6 = geometry_msgs.msg.Pose()
    #ur5_pose_6.position.x = 0.817165
    #ur5_pose_6.position.y = 0.213639
    #ur5_pose_6.position.z = 0.944145
    #ur5_pose_6.orientation.x = 1.570943
    #ur5_pose_6.orientation.y = -0.000478
    #ur5_pose_6.orientation.z = -3.141480
   
    while not rospy.is_shutdown():
	
        #ur5.go_to_pose(ur5_pose_1)
        #rospy.sleep(2)
       # ur5.go_to_pose(ur5_pose_2)
       # rospy.sleep(2)
        ur5.go_to_pose(ur5_pose_3)
        rospy.sleep(2)
	ur5.attach_box()
	rospy.sleep(1)
        vacuum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vacuum_gripper(True)
        rospy.sleep(2)
	ur5.go_to_pose(ur5_pose_5)
        rospy.sleep(2)
	ur5.go_to_pose(ur5_pose_4)
        rospy.sleep(2)
        vacuum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vacuum_gripper(False)
	#ur5.go_to_pose(ur5_pose_6)
        #rospy.sleep(2)
	ur5.go_to_predefined_pose("allZeros")
        rospy.sleep(2)
    del ur5


if __name__ == '__main__':
    main()


