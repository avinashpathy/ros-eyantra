#! /usr/bin/env python

import rospy
import sys
import copy

import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
import pkg_vb_sim
#from logical_camera_2 import pose
from hrwros_gazebo.msg import LogicalCameraImage
from pkg_vb_sim.srv import conveyorBeltPowerMsg
from hrwros_gazebo.msg import Model
from  pkg_vb_sim.srv import vacuumGripper
#from LogicalCameraImage.msg import Pose
class CartesianPath:
    # Constructor
    def __init__(self):
        rospy.init_node('node_eg5_waypoints', anonymous=True)
        rospy.Subscriber("/eyrc/vb/logical_camera_2",LogicalCameraImage,self.callback)
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
        self.constart()
        rospy.loginfo('\033[94m' + " >>> Init done." + '\033[0m')

    def ee_cartesian_translation(self, trans_x, trans_y, trans_z):
        # 1. Create a empty list to hold waypoints
        waypoints = []

        # 2. Add Current Pose to the list of waypoints
        waypoints.append(self._group.get_current_pose().pose)

        # 3. Create a New waypoint
        wpose = geometry_msgs.msg.Pose()
        wpose.position.x = waypoints[0].position.x + (trans_x)
        wpose.position.y = waypoints[0].position.y + (trans_y)
        wpose.position.z = waypoints[0].position.z + (trans_z)
        # This to keep EE parallel to Ground Plane
        wpose.orientation.x = -0.5
        wpose.orientation.y = -0.5
        wpose.orientation.z = 0.5
        wpose.orientation.w = 0.5


        # 4. Add the new waypoint to the list of waypoints
        waypoints.append(copy.deepcopy(wpose))


        # 5. Compute Cartesian Path connecting the waypoints in the list of waypoints
        (plan, fraction) = self._group.compute_cartesian_path(
            waypoints,   # waypoints to follow
            0.01,        # Step Size, distance between two adjacent computed waypoints will be 1 cm
            0.0)         # Jump Threshold
        rospy.loginfo("Path computed successfully. Moving the arm.")

        # The reason for deleting the first two waypoints from the computed Cartisian Path can be found here,
        # https://answers.ros.org/question/253004/moveit-problem-error-trajectory-message-contains-waypoints-that-are-not-strictly-increasing-in-time/?answer=257488#post-id-257488
        num_pts = len(plan.joint_trajectory.points)
        if (num_pts >= 3):
            del plan.joint_trajectory.points[0]
            del plan.joint_trajectory.points[1]

        # 6. Make the arm follow the Computed Cartesian Path
        self._group.execute(plan)


    def go_to_pose(self, arg_pose):

        pose_values = self._group.get_current_pose().pose
        #rospy.loginfo('\033[94m' + ">>> Current Pose:" + '\033[0m')
        #rospy.loginfo(pose_values)

        self._group.set_pose_target(arg_pose)
        flag_plan = self._group.go(wait=True)  # wait=False for Async Move

        pose_values = self._group.get_current_pose().pose
        #rospy.loginfo('\033[94m' + ">>> Final Pose:" + '\033[0m')
        #rospy.loginfo(pose_values)

        list_joint_values = self._group.get_current_joint_values()
        #rospy.loginfo('\033[94m' + ">>> Final Joint Values:" + '\033[0m')
        #rospy.loginfo(list_joint_values)

        if (flag_plan == True):
            rospy.loginfo('\033[94m' + ">>> go_to_pose() Success" + '\033[0m')
        else:
            rospy.logerr(
                '\033[94m' + ">>> go_to_pose() Failed. Solution for Pose not Found." + '\033[0m')



        return flag_plan


    # Destructor
    def __del__(self):
        moveit_commander.roscpp_shutdown()
        rospy.loginfo(
            '\033[94m' + "Object of class CartesianPath Deleted." + '\033[0m')

    def callback(self,msg):
	#this is called everytime a message is detected by the subscriber
        try:
            for i in range(3):
                if(msg.models[i].type=="packagen1"):
		    if(((msg.models[i].pose.position.y)>-0.05) and ((msg.models[i].pose.position.y)<0.05)):
             		#called the constop function when the package is in the range
	                self.constop(1)
 		if(msg.models[i].type=="packagen2"):
		    if(((msg.models[i].pose.position.y)>-0.05) and ((msg.models[i].pose.position.y)<0.05)):
                       
	                self.constop(2)
		if(msg.models[i].type == "packagen3"):
		    
		    if(((msg.models[i].pose.position.y) > -0.05) and ((msg.models[i].pose.position.y)< 0.05)):
			self.constop(3)
	except:
	    pass
    def constart(self):
	#function to start conveyer belt
        conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
	conveyor_belt(30)
    def constop(self,number):
	#function to stop the conveyer belt
	conveyor_belt=rospy.ServiceProxy("/eyrc/vb/conveyor/set_power",conveyorBeltPowerMsg)
	conveyor_belt(0)
        ur5_4_home_pose = geometry_msgs.msg.Pose()
        ur5_3_home_pose = geometry_msgs.msg.Pose()
	box_name = "packagen1"
	box_name1 = "packagen2"
	box_name2 = "packagen3"
	#argument number passed based on the package detected by the logical camera
	#number = 1 implies packagen1
	#number = 2 implies packagen2
	#number = 3 implies packagen3
        if(number==1):
            self.act_vac()
	    self.ee_cartesian_translation(0.726,0.38,-0.068)
            ur5_3_home_pose.position.x = 0.11
            ur5_3_home_pose.position.y = 0.65
            ur5_3_home_pose.position.z = 1.2
	    ur5_3_home_pose.orientation.x = -0.5
            ur5_3_home_pose.orientation.y = -0.5
            ur5_3_home_pose.orientation.z = 0.5
            ur5_3_home_pose.orientation.w = 0.5
            self.dact_vac()
	    #rospy.sleep(3)
	    self.constart()
            
        if(number==2):
            #ur5_4_home_pose.position.x = -0.66
            #ur5_4_home_pose.position.y = 0.00
            #ur5_4_home_pose.position.z = 1.19
            #ur5_4_home_pose.orientation.x = -0.5
            #ur5_4_home_pose.orientation.y = -0.5
            #ur5_4_home_pose.orientation.z = 0.5
            #ur5_4_home_pose.orientation.w = 0.5
            self.ee_cartesian_translation(0.14,0,0)
            self.act_vac()
	    ur5_4_home_pose.position.x = 0.75
            ur5_4_home_pose.position.y = 0.0
            ur5_4_home_pose.position.z = 1.2
            ur5_4_home_pose.orientation.x = -0.5
            ur5_4_home_pose.orientation.y = -0.5
            ur5_4_home_pose.orientation.z = 0.5
            ur5_4_home_pose.orientation.w = 0.5
	    attached_objects = self._scene.get_attached_objects()
	    #print("printing attached objects >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	    #print(attached_objects)
	    is_attached = len(attached_objects.keys()) > 0
	    objects = self._scene.get_objects()
	    print("*******************************************")
	    print(objects)
	    print("###########################################")
	    if(is_attached):
            	self.go_to_pose(ur5_4_home_pose)
	    	self.constart()
	    	self.dact_vac()
	    	#self.ee_cartesian_translation(-0.714,0.213,0.912)
            
        if(number==3):
            ur5_4_home_pose.position.x = 0.04
            ur5_4_home_pose.position.y = -0.65
            ur5_4_home_pose.position.z = 1.2
           
            ur5_2_home_pose = geometry_msgs.msg.Pose()
	    ur5_2_home_pose.orientation.x = -0.5
    	    ur5_2_home_pose.orientation.y = -0.5
   	    ur5_2_home_pose.orientation.z = 0.5
    	    ur5_2_home_pose.orientation.w = 0.5
    	    ur5_2_home_pose.position.z = 1 

            self.ee_cartesian_translation(-0.2,0,0)
            self.act_vac()
	    attached_objects = self._scene.get_attached_objects()
	    is_attached = len(attached_objects.keys()) > 0
	    if(is_attached):
            	self.go_to_pose(ur5_4_home_pose)
            	self.dact_vac()
        
    def act_vac(self):
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vaccum_gripper(True)
    def dact_vac(self):
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5_1/activate_vacuum_gripper",vacuumGripper)
        vaccum_gripper(False)
def main():
    ur5 = CartesianPath()
    box_length = 0.15               # Length of the Package
    vacuum_gripper_width = 0.115    # Vacuum Gripper Width
    delta = vacuum_gripper_width + (box_length/2)  # 0.19
    # Teams may use this info in Tasks
    ur5_2_home_pose = geometry_msgs.msg.Pose()#this is the line of error, attribute error
    ur5_2_home_pose.position.x = -0.8 
    ur5_2_home_pose.position.y = 0
    ur5_2_home_pose.position.z = 1 + vacuum_gripper_width + (box_length/2)
    # This to keep EE parallel to Ground Plane
    ur5_2_home_pose.orientation.x = -0.5
    ur5_2_home_pose.orientation.y = -0.5
    ur5_2_home_pose.orientation.z = 0.5
    ur5_2_home_pose.orientation.w = 0.5
    ur5.go_to_pose(ur5_2_home_pose)
    box_name = "packagen1"
    box_name1 = "packagen2"
    box_name2 = "packagen3"
    while not rospy.is_shutdown():
        # 1. Go to Home Position
	#x = ur5._group.get_current_pose().pose.position.x
	#y = ur5._group.get_current_pose().pose.position.y
	#z = ur5._group.get_current_pose().pose.position.z
	#if(x > 0.12 and x < 0.10 and y > 0.66 and y < 0.64 and z > 1.21 and z < 1.19):
	attached_objects = ur5._scene.get_attached_objects()
	is_attached = len(attached_objects.keys()) > 0
        is_known = box_name in ur5._scene.get_known_object_names()
	#print("main main main amianmain main main main main main maina main mani amin")
	#print(is_known)
        if not is_attached:
		ur5.go_to_pose(ur5_2_home_pose)
	
    del ur5


if __name__ == '__main__':

    main()