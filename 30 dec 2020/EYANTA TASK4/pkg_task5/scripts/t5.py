#! /usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import actionlib
import rospkg
import sys
import copy
import json
import requests
import time
from pkg_vb_sim.srv import conveyorBeltPowerMsg
from hrwros_gazebo.msg import Model
from  pkg_vb_sim.srv import vacuumGripper
from moveit_commander import MoveGroupCommander, roscpp_initialize
import cv2
from pkg_task4.msg import msgFile
from pkg_task4.msg import state_msg
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pkg_ros_iot_bridge.msg import msgRosIotAction      # Message Class that is used by ROS Actions internally
from pkg_ros_iot_bridge.msg import msgRosIotGoal        # Message Class that is used for Goal Messages
from pkg_ros_iot_bridge.msg import msgRosIotResult      # Message Class that is used for Result Messages
from pkg_ros_iot_bridge.msg import msgMqttSub
import datetime                                   

import numpy as np
from pyzbar.pyzbar import decode
item = dict()
power_val = 90                                                            #stores the power value for the conveyor belt
pack_av = dict()                                                  
pack =dict()                                                              #dictionary that stores package name and colour
flag = True
flag1 = False
p=dict	()
order_id = 0
order_ls = []
order_no = 0
dict1 = {'Medicine' : 'red', 'Clothes' : 'green', 'Food' : 'yellow'}
URL = "https://script.google.com/macros/s/AKfycbx4_KSB3dGiZOL_ExE1DJ_x1RrLXo2-onAlmf9jL6Ksmshvnuael-y6mw/exec"


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
      

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        (rows,cols,channels) = cv_image.shape
        
        image = cv_image
        global flag
       
        for i in range (4):                                                                 #package in different row and column number is recognised using cropping technique

            for j in range (3):
                
                image =cv_image[(300+i*150):(450+i*150),(110+j*190):(250+j*190)]
                
                colour = self.pkg_color(image)

                if(flag):

                    pack["package{}{}".format(i,j)] = colour 
                                                     # pkg_colour with package name    
                
                
            rospy.sleep(1)
        flag = False 
        print(pack)
        cv2.waitKey(3)

    def pkg_color(self,arg_img):
        qr_result = decode(arg_img)

        if ( len( qr_result ) > 0):
    
            return (qr_result[0].data)
        
        else :
            return ('NA')

   
    def vacuum_griper(self,state):                                                       #function to activate and deactivate the vacuum gripper
         
        vaccum_gripper=rospy.ServiceProxy("/eyrc/vb/ur5/activate_vacuum_gripper/ur5_1",vacuumGripper)
        vaccum_gripper(state)


          
    def pkg_pose(self , joint_angles1 , joint_angles2):                                         #fun
    
        res = self.set_joint_angles(joint_angles1)
        if (res == False):                                                                      #if fails to go to near package goes to all zeros pose and then plans the path to go near package
            self.vacuum_griper(False)
	    rospy.sleep(0.2)
            print("Failed to go to near package !")
            self.go_to_predefined_pose("allZeros")
            rospy.sleep(0.2)
            self.set_joint_angles(joint_angles1)
        rospy.sleep(0.5)

        self.vacuum_griper(True)                                                                #activating vacuum griper

        self.set_joint_angles(joint_angles2)
        rospy.sleep(0.5)

    def pkg_con_pose(self,con_joint_angles):
    
        res = self.set_joint_angles(con_joint_angles)
        if(res == False):
            rospy.sleep(0.2)                                                                   #if fails to go to near package goes to all zeros pose and then plans the path to go near conveyor belt
            print("Failed to go to converyor belt !")
            self.go_to_predefined_pose("allZeros")
            rospy.sleep(0.2)
            self.set_joint_angles(con_joint_angles)
            rospy.sleep(0.2)

        self.vacuum_griper(False)
        rospy.sleep(1)

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

def inventory_push():
    global pack
    global pack_av
    global URL
    x = datetime.datetime.now()
    m = str(x.strftime("%m"))
    y = str(x.strftime("%y"))
    d = str(x.strftime("%c"))

    storage_no = {"package00":"R0 C0", "package01":"R0 C1", "package02":"R0 C2", "package10":"R1 C0", "package11" : "R1 C1", "package12" : "R1 C2", "package21" : "R2 C1", "package22" : "R2 C2", "package20" : "R2 C0", "package30" : "R3 C0", "package31" : "R3 C1", "package32" : "R3 C2"}
    cost = {"red":450, "yellow" : 250 , "green" : 150}

    priority = {"red" : "HP", "yellow" : "MP", "green" : "LP"}

    item = {"red" : "Medicine", "yellow" : "Food", "green" : "Clothes"}

    sku = {"red" : "R", "yellow" : "Y", "green" : "G"}
    rospy.sleep(3)
    for i in range (12):
	print(pack.keys()[i])
# defining our sheet name in the 'id' variable and the the column where we want to update the value
        parameters = {"id":"Inventory","Timestamp" : d, "Team Id":"VB#0865", "Unique Id":"aBCaRvEc", "SKU": sku[pack[pack.keys()[i]]] + pack.keys()[i][7:]+m+y , "Item": item[pack[pack.keys()[i]]], "Priority": priority[pack[pack.keys()[i]]], "Storage Number":storage_no[pack.keys()[i]], "Cost": cost[pack[pack.keys()[i]]], "Quantity":"1"} 

	
	response = requests.get(URL, params=parameters)

	print(response.content)
    pack_av = pack.copy()
    pack_av.pop('package30')
    pack_av.pop('package31')
    pack_av.pop('package21')
    print("The availabe packages coordinates -")
    print(pack_av)

#getting date and time
def get_time_str():
    timestamp = int(time.time())
    value = datetime.datetime.fromtimestamp(timestamp)
    str_time = value.strftime('%m/%d/%Y %H:%M:%S')
    return str_time


#dispatched status
def dispatched(flag):
    global order_id
    global p
    global order_ls
    global URL
    cost = {"Medicine":450, "Food" : 250 , "Clothes" : 150}

    priority = {"Medicine" : "HP", "Food" : "MP", "Clothes" : "LP"}

    if(flag):
    	for i in range(len(p)):
	    if(p.keys()[i]==order_id):
		ls = p.values()[i]
		print("******LIST******")
		print(ls)
		break
		 
	time = get_time_str()

    	parameters = {"id":"OrdersDispatched", "Team Id":"#VB0865", "Unique Id": "aBCaRvEc", "Order ID":order_id,"City":ls[1], "Item":ls[4],"Priority":priority[ls[4]], "Dispatch Quantity":ls[0],"Cost":cost[ls[4]], "Dispatch Status":"YES", "Dispatch Date and Time":time} 

    	
    	response = requests.get(URL, params=parameters)

    	print(response.content)
	order_ls.append(order_id)
	

def estimated_time(pack_prio):
    timestamp = int(time.time())
    value = datetime.datetime.fromtimestamp(timestamp)
    
    if (pack_prio == 'Medicine'):
	
	value = value + datetime.timedelta(days = 1)
    
    elif (pack_prio == 'Food'):
	
	value = value + datetime.timedelta(days = 3)
     
    elif (pack_prio == 'Clothes'):
	
	value = value + datetime.timedelta(days = 5)
   
    str_time = value.strftime('%Y-%m-%d')
    return str_time

def shipped(condition):
    global p
    global order_ls
    global order_no
    global URL
    cost = {"Medicine":450, "Food" : 250 , "Clothes" : 150}

    priority = {"Medicine" : "HP", "Food" : "MP", "Clothes" : "LP"}

    if(condition):
    	ls = p[order_ls[order_no]]
	time = get_time_str()
	est_time = estimated_time(ls[4])

    	parameters = {"id":"OrdersShipped", "Team Id":"#VB0865", "Unique Id": "aBCaRvEc", "Order ID":order_ls[order_no],"City":ls[1], "Item":ls[4],"Priority":priority[ls[4]], "Shipped Quantity":ls[0],"Cost":cost[ls[4]], "Shipped Status":"YES", "Shipped Date and Time":time , "Estimated Time of Delivery":est_time } 

    
    	response = requests.get(URL, params=parameters)

    	print(response.content)
	order_no = order_no + 1
	flag = False



def start(my_msg):
    global p
    global item
    global URL
    print("The message is : ")
    
    print('_____________________')

    res = json.loads(my_msg.message)
    item[res['item']]=res['order_id']
    #res.decode("utf-8")
    p[res['order_id']] = res['qty'],res['city'],res['lon'],res['lat'],res['item']
    
    sheet(res)
     
def sheet(res1):
# defining our sheet name in the 'id' variable and the the column where we want to update the value
    global flag1
    global URL
    
    cost = {"Medicine":450, "Food" : 250 , "Clothes" : 150}

    priority = {"Medicine" : "HP", "Food" : "MP", "Clothes" : "LP"}
    
    flag1 = True

    parameters = {"id":"IncomingOrders", "Team Id":"#VB0865", "Unique Id": "aBCaRvEc", "Order ID":res1['order_id'], "Order Date and Time":res1['order_time'], "Item":res1['item'],"Priority":priority[res1['item']],
 "Order Quantity": res1["qty"], "City":res1['city'], "Longitude":res1['lon'], "Latitude":res1["lat"], "Cost":cost[res1['item']]}
    
    headers = {
        'Authorization': "Bearer [token]"
    	}
    parameters_1 = {'id':'Dashboard' ,'Item':res1['item'] , 'Priority':priority[res1['item']] , 'City':res1['city'] , 'Order Date and Time':res1['order_time']}

    response = requests.get(URL, params=parameters,headers=headers)
    response1 = requests.get(URL, params=parameters_1,headers=headers)

    print(response.content)
    
    print(response1.content)

#function to service the order based on priority    
def priority():
    global order_id
    global pack_av	
    global dict1
    global item
    item.keys().sort(reverse = True)			
    for i in range(len(item)): 
        for package,color in pack_av.items():
            if(dict1[item.keys()[i]] == color): 
		order_id = item.values()[i]		            		
		print("Order id is - ",order_id)
		item.pop(item.keys()[i])
                return package

def func_callback(myMsg):
    if(myMsg.state):
	print("The order has been shipped !")
	shipped(True)

def main():

    var_handle_pub = rospy.Publisher('my_topic', msgFile, queue_size=10)      #publisher topic for publishing colour
    rospy.Subscriber("/ros_iot_bridge/mqtt/sub",msgMqttSub,start)
    rospy.Subscriber('state_topic', state_msg, func_callback)

    obj_msg = msgFile()
    
    #First row
    #lst_joint_angles_00 = [-0.267,-2.39,1.094,-1.856,-1.29,1.489]      #package00
    lst_joint_angles_00 = [-0.909,-1.204,0.14,-1.921,-2.1488,0.538]
    lst_joint_angles_00_0 =[-0.607,-1.415,0.361,-1.8763,-2.478,0.619]
  
    
    lst_joint_angles_01 = [2.251,-1.5389,-0.588,-1.0716,0.8915,0]      #package01
    lst_joint_angles_01_0 = [2.615,-1.3736,-0.378,-1.381,-1.9714,-0.0569]
    
    lst_joint_angles_02 = [1.0571,-1.8535,-0.2083,-1.0797,2.0845,0.0962]      #package02
    lst_joint_angles_02_0 = [0.616,-1.5909,-0.555,-0.9954,2.5255,0.0961]

    #second row
    lst_joint_angles_10 = [-0.849887,-1.43650,0.828597,0.607385,2.274718,-0.000851]            #package10
    lst_joint_angles_10_0 = [-0.58680,-1.57314,0.977149,0.595126,2.537753,-0.00103]

    lst_joint_angles_11 = [-2.01037,-1.889515,1.1925625,0.6969144,1.067172,-1.5003408]          #package11
    lst_joint_angles_11_0 = [-2.85409,-2.166812,1.28145,0.885655,0.223412,-1.500694]

    lst_joint_angles_12 = [1.030,-1.404,-1.4686,-0.242,2.079,-1.541]         #package12
    lst_joint_angles_12_0 = [0.6119,-1.2189,-1.61065,-0.2737,2.498,-1.522]
   
    #third row
    lst_joint_angles_20 = [-0.8969,-1.6420,1.9698,2.8133,-2.245,0.0969]      #package20
    lst_joint_angles_20_0 = [-0.6064,-1.7692,2.0942,2.8158,-2.5352,0.09676]
   
    lst_joint_angles_22 = [0.96,-1.4543,-2.0611,0.3755,2.1740,0]             #package22
    lst_joint_angles_22_0 = [0.626,-1.2921,-2.187,0.3398,2.5152,0.001]
    #lst_joint_angles_22_1 = [0.626,-1.2921,-2.187,0.3376,0.9422,0.001]   
    #fourth row
    lst_joint_angles_32 = [0.9882,-1.516,-2.131,-2.656,-2.356,0.005]      #package32
    lst_joint_angles_32_0 = [0.7057,-1.3916,-2.2327,-2.687,-2.518,-0.005]
    #lst_joint_angles_32_1 = [0.7057,-1.3899,-2.2341,-2.68,-0.877,-0.005] 

    #convey_belt pose joint angles
    lst_joint_angles = [0,-2.2846,-1.146,-1.282,1.565,-1.572]    
     

    package = pkg_sort()
    global pack
    global pack_av 								#package dictionary that stores the available package coordinates
    rospy.sleep(3)
    inventory_push()								#calling function to push data to inventory
    global flag1
    while not rospy.is_shutdown():
    	while (flag1):
	    package_name = priority()
	    if package_name != None :
                print(package_name)
            if(package_name == 'package02'):                                                                        #first package
		package.pkg_pose(lst_joint_angles_02,lst_joint_angles_02_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package02"]
		obj_msg.name = "packagen02"
		rospy.loginfo(obj_msg)
		dispatched(True)										    #calling function to update data on dispatched sheet

            if(package_name == 'package01'):                                                                        #second package
		package.pkg_pose(lst_joint_angles_01,lst_joint_angles_01_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package01"]
		obj_msg.name = "packagen01"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package00'):                                                                        #third package
		package.pkg_pose(lst_joint_angles_00,lst_joint_angles_00_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package00"]
		obj_msg.name = "packagen00"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package12'):                                                                        #fourth package
		package.pkg_pose(lst_joint_angles_12,lst_joint_angles_12_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package12"]
		obj_msg.name = "packagen12"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package11'):                                                                        #five package
		package.pkg_pose(lst_joint_angles_11,lst_joint_angles_11_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package11"]
		obj_msg.name = "packagen11"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package10'):                                                                        #six package
		package.pkg_pose(lst_joint_angles_10,lst_joint_angles_10_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package10"]
		obj_msg.name = "packagen10"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package20'):                                                                        #seven package
		package.pkg_pose(lst_joint_angles_20,lst_joint_angles_20_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package20"]
		obj_msg.name = "packagen20"
		rospy.loginfo(obj_msg)
		dispatched(True)

            if(package_name == 'package22'):                                                                        #eight package
		package.pkg_pose(lst_joint_angles_22,lst_joint_angles_22_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package22"]
		obj_msg.name = "packagen22"
		rospy.loginfo(obj_msg)
		dispatched(True)


            if(package_name == 'package32'):                                                                        #nine package
		package.pkg_pose(lst_joint_angles_32,lst_joint_angles_32_0)
		rospy.sleep(0.5)
		package.pkg_con_pose(lst_joint_angles)
		obj_msg.col = pack["package32"]
		obj_msg.name = "packagen32"
		rospy.loginfo(obj_msg)
		dispatched(True)
	    val = pack_av.pop(package_name,-1)
	    	
    	    var_handle_pub.publish(obj_msg)                                                     #publishes the package name
  
	
    del package

if __name__ == '__main__':

    main()



#problems to be solved
#order gets unserviced


