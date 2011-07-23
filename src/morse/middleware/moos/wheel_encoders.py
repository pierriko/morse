import pymoos.MOOSCommClient
import morse.core.middleware
import GameLogic
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
    print('######## Wheel Encoers-SENSOR INITIALIZED ########')

def post_wheel_encoders(self, component_instance):
    """ Publish the data of the Odometry-sensor as a ROS-Pose message
    """
    curTime=pymoos.MOOSCommClient.MOOSTime()

    if (component_instance.local_data['numWheels']==2):
        self.m.Notify('zE_fr',component_instance.local_data['rotFR'],curTime)
        self.m.Notify('zE_fl',component_instance.local_data['rotFL'],curTime)
    elif (component_instance.local_data['numWheels']==4):
        self.m.Notify('zE_fr',component_instance.local_data['rotFR'],curTime)
        self.m.Notify('zE_fl',component_instance.local_data['rotFL'],curTime)
        self.m.Notify('zE_rr',component_instance.local_data['rotRR'],curTime)
        self.m.Notify('zE_rl',component_instance.local_data['rotRL'],curTime)
