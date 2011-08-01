import logging; logger = logging.getLogger("morse." + __name__)
import roslib; roslib.load_manifest('roscpp'); roslib.load_manifest('rospy'); roslib.load_manifest('geometry_msgs'); roslib.load_manifest('sensor_msgs')
import rospy
import std_msgs
import sys
import traceback
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
import GameLogic
import math
import mathutils

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    # Compose the name of the port, based on the parent and module names
    component_name = component_instance.blender_obj.name
    parent_name = component_instance.robot_parent.blender_obj.name

     # Add the new method to the component
    component_instance.output_functions.append(function)

    # Generate one publisher and one topic for each component that is a sensor and uses post_message
    if mw_data[1] == "post_velocity_twist":  
        self._topics.append(rospy.Publisher(parent_name + "/" + component_name, Twist))
    elif mw_data[1] == "post_imu":
        self._topics.append(rospy.Publisher(parent_name + "/" + component_name, Imu))

    logger.info('Initilized IMU Publishing on topic: /' + parent_name + "/" + component_name)

def post_imu(self, component_instance):
    """Publish the data as an IMU message.
    """
    try:
        data = component_instance.local_data
        parent_name = component_instance.robot_parent.blender_obj.name
        msg = Imu()
        
        msg.header.stamp = rospy.Time.from_sec(GameLogic.current_sim_time)
        msg.header.frame_id = "imu_link"
        msg.angular_velocity.x = data['velocity'][3]
        msg.angular_velocity.y = data['velocity'][4]
        msg.angular_velocity.z = data['velocity'][5]
        msg.linear_acceleration.x = data['acceleration'][0]
        msg.linear_acceleration.y = data['acceleration'][1]
        msg.linear_acceleration.z = data['acceleration'][2]
        
        for topic in self._topics:
            if str(topic.name) == str("/"+parent_name+"/"+component_instance.blender_obj.name):
                topic.publish(msg)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

def post_velocity_twist(self, component_instance):
    """ Publish the data of the Odometry-sensor as a ROS-Pose message
    """
    parent_name = component_instance.robot_parent.blender_obj.name
    twist = Twist()
    
    # Fill twist-msg with the values from the sensor
    twist.linear.x = component_instance.local_data['velocity'][0]
    twist.linear.y = component_instance.local_data['velocity'][1]
    twist.linear.z = component_instance.local_data['velocity'][2]
    twist.angular.x =component_instance.local_data['velocity'][3]
    twist.angular.y =  component_instance.local_data['velocity'][4]
    twist.angular.z = component_instance.local_data['velocity'][5]
    
    for topic in self._topics: 
        # publish the message on the correct topic    
        if str(topic.name) == str("/" + parent_name + "/" + component_instance.blender_obj.name):
            topic.publish(twist)
