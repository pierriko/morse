import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
import morse.core.middleware

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
    logger.info('######## GPS-SENSOR INITIALIZED ########')

def post_gps(self, component_instance):
    """ Publish the data of the Odometry-sensor as a ROS-Pose message
    """
    #curTime=pymoos.MOOSCommClient.MOOSTime()
    curTime=self.current_MOOS_time
    parent_name = component_instance.robot_parent.blender_obj.name
    
    self.m.Notify('zEast',component_instance.local_data['x'],curTime)
    self.m.Notify('zNorth',component_instance.local_data['y'],curTime)
    self.m.Notify('zHeight',component_instance.local_data['z'],curTime)
    self.m.Notify('zCourse', component_instance.local_data['course'],curTime)
    self.m.Notify('zHorizSpeed', component_instance.local_data['speed'],curTime)
    self.m.Notify('zVertVel', component_instance.local_data['vertSpeed'],curTime)
    self.m.Notify('zVelXGPS',component_instance.local_data['velX'],curTime)
    self.m.Notify('zVelYGPS',component_instance.local_data['velY'],curTime)
    self.m.Notify('zVelZGPS',component_instance.local_data['velZ'],curTime)
    
