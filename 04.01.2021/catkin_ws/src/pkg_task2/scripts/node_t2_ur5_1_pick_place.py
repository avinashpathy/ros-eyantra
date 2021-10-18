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
        self._flag_pickable = False
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

    def add_box(self, timeout=4):			#function to add box in rviz in the planning scene
	
	box_name = self.box_name
	scene = self._scene
        box_pose = geometry_msgs.msg.PoseStamped()
	box_pose.header.frame_id = "world"
	
	box_pose.pose.orientation.w = 1
	box_pose.pose.position.x = 0.038314
	box_pose.pose.position.y = 0.453061
	box_pose.pose.position.z = 1.865431 
	box_name = "box"
	scene.add_box(box_name, box_pose, size=(0.15, 0.15, 0.15))

	self.box_name=box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)
  

    def attach_box(self, timeout=4):		       #function to attach box in rviz in the planning scene
   
	box_name = self.box_name
	robot = self._robot
	scene = self._scene
	eef_link = self._eef_link
	group_names = self._group_names

	grasping_group = 'ur5_1_planning_group'
	touch_links = robot.get_link_names(group=grasping_group)
        scene.attach_box(eef_link, box_name, touch_links=touch_links)
	
   
    
    def go_to_predefined_pose(self, arg_pose_name):		#function to go to the predefined position
        rospy.loginfo('\033[94m' + "Going to Pose: {}".format(arg_pose_name) + '\033[0m')
        self._group.set_named_target(arg_pose_name)
        plan = self._group.plan()
        goal = moveit_msgs.msg.ExecuteTrajectoryGoal()
        goal.trajectory = plan
        self._exectute_trajectory_client.send_goal(goal)
        self._exectute_trajectory_client.wait_for_result()
        rospy.loginfo('\033[94m' + "Now at Pose: {}".format(arg_pose_name) + '\033[0m')

    def detach_box(self, timeout=4):				#function to detach the box from the arm in the planning scene

	box_name = self.box_name
	scene = self._scene
	eef_link = self._eef_link
        scene.remove_attached_object(eef_link, name=box_name)
  
        return self.wait_for_state_update(box_is_known=True, box_is_attached=False, timeout=timeout)


    def remove_box(self, timeout=4):				#function to remove box from the arm in the planning scene
        box_name = self.box_name
        scene = self._scene
        scene.remove_world_object(box_name)
        return self.wait_for_state_update(box_is_attached=False, box_is_known=False, timeout=timeout)
   
    
    # Destructor
    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class Ur5Moveit Deleted." + '\033[0m')


def main():

    ur5 = Ur5Moveit()
    
    #calling add box function to add box in the rviz planning scene
    ur5.add_box()
    
    #giving coordinates of the required position for arm to plan the path
    #Position 1
 
    ur5_pose_3 = geometry_msgs.msg.Pose()
    ur5_pose_3.position.x = 0.018298
    ur5_pose_3.position.y = 0.260411
    ur5_pose_3.position.z = 1.911618
 
    #Position 2
    ur5_pose_4 = geometry_msgs.msg.Pose()
    ur5_pose_4.position.x = -0.57560
    ur5_pose_4.position.y = -0.348486
    ur5_pose_4.position.z = 1.464110
    ur5_pose_4.orientation.x = 0.00038656093817
    ur5_pose_4.orientation.y = -0.000299172174753
    ur5_pose_4.orientation.z = -2.44215307546e-05
    ur5_pose_4.orientation.w = 0.999999880235
     
    
      
    ur5.go_to_pose(ur5_pose_3)
    rospy.sleep(2)
   
    #calling attach box function to attach box to the arm in the planning scene
    ur5.attach_box()
    
    #calling the rosservice to activate vacuum gripper when arm reaches near the box 
    vacuum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
    rospy.sleep(1)
    
    #vacuum gripper is activated
    vacuum_gripper(True)
 
  
    ur5.go_to_pose(ur5_pose_4)
    rospy.sleep(1)

      
    #calling the rosservice to  deactivate vacuum gripper when arm reaches near the Bin
    vacuum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
    
    #vacuum gripper is deactivated
    vacuum_gripper(False)
   
    #calling detach box function to detach box from the arm in the planning scene 
    ur5.detach_box()
    
    #calling remove box function to remove box from the arm in the planning scene
    ur5.remove_box()
  
    #arm going to allZeros position (Initial Position)
    ur5.go_to_predefined_pose("allZeros")
    rospy.sleep(2)


if __name__ == '__main__':
    main()
  



  

    

   

   
   
   
	
    



