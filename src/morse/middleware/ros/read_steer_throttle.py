import roslib; roslib.load_manifest('roscpp'); roslib.load_manifest('rospy'); roslib.load_manifest('geometry_msgs'); roslib.load_manifest('rosgraph_msgs'); roslib.load_manifest('morse_scripts')
import rospy
import std_msgs
import math
from morse_scripts.msg import SteerThrottle

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    component_name = component_instance.blender_obj.name
    parent_name = component_instance.robot_parent.blender_obj.name
    
    # Add the new method to the component
    component_instance.input_functions.append(function)
    self._topics.append(rospy.Subscriber(parent_name + "/" + component_name, SteerThrottle, callback_wp, component_instance))

def callback_wp(data, component_instance):
        """ this function is called as soon as Twist messages are published on the specific topic """
        component_instance.local_data["force"] = data.throttle
        component_instance.local_data["steer"] = data.steer
        component_instance.local_data["brake"] = 0.1 # Constant brake to prevent rolling to a stop.
        
def read_steer_throttle(self, component_instance):
        """ dummy function for Waypoints """
        pass
