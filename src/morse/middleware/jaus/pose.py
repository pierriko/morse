import logging; logger = logging.getLogger("morse." + __name__)
import pyOpenJAUS.GposComponent
import pyOpenJAUS.mobility
import morse.core.middleware
import GameLogic

def init_extra_module(self, component_instance, function, mw_data):
    """ Create a JAUS component to provide the Global Position service
    """
    # Compose the name of the port, based on the parent and module names
    component_name = component_instance.blender_obj.name
    parent_name = component_instance.robot_parent.blender_obj.name

    # Add the new method to the component
    component_instance.output_functions.append(function)

    # create a JAUS global pose sensor
    self.m=pyOpenJAUS.GposComponent.GposComponent()
    self.m.setName("MORSE_Sim_Pose")
    self.m.run()

    # create SetGlobalPose message to update GPos position
    self.curPos=pyOpenJAUS.mobility.SetGlobalPose()
    self.curPos.enableLatitude()
    self.curPos.enableLongitude()
    self.curPos.enableAltitude()
    self.curPos.enablePositionRms()
    self.curPos.enableRoll()
    self.curPos.enablePitch()
    self.curPos.enableYaw()

    # Generate one publisher and one topic for each component that is a sensor and uses post_message
    logger.info('######## POSE-SENSOR INITIALIZED ########')

def post_pose(self, component_instance):
    """ Publish the data of the Odometry-sensor as a ROS-Pose message
    """
    #curTime=self.current_MOOS_time
    parent_name = component_instance.robot_parent.blender_obj.name
    
    # post the robot position
    # TODO: CONVERT THIS TO LATITUDE AND LONGITUDE
    self.curPos.setLatitude_deg(component_instance.local_data['x'])
    self.curPos.setLongitude_deg(component_instance.local_data['y'])
    self.curPos.setAltitude_m(component_instance.local_data['z'])
    self.curPos.setPositionRms_m(0.0)
    self.curPos.setRoll_rad(component_instance.local_data['yaw'])
    self.curPos.setPitch_rad(component_instance.local_data['roll'])
    self.curPos.setYaw_rad(component_instance.local_data['pitch'])

    self.m.updateGlobalPose(self.curPos)
