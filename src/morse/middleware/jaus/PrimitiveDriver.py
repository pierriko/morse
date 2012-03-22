import logging; logger = logging.getLogger("morse." + __name__)
import pyOpenJAUS.pyComponents
import pyOpenJAUS.mobility
import morse.core.middleware
import GameLogic

def init_extra_module(self, component_instance, function, mw_data):
    """ Create a JAUS component to provide the Primitive Driver service
    """
    # Compose the name of the port, based on the parent and module names
    component_name = component_instance.blender_obj.name
    parent_name = component_instance.robot_parent.blender_obj.name

    # Add the new method to the component
    component_instance.input_functions.append(function)

    # create a JAUS global pose sensor
    self.m=pyOpenJAUS.pyComponents.PrimitiveDriverComponent()
    self.m.setName("MORSE_Sim_Primitive_Driver")
    self.m.run()

    # create Query message to read current wrench effort
    self.qryWrench=pyOpenJAUS.mobility.QueryWrenchEffort()
    self.qryWrench.setPresenceVector(65546);

    self.curWrenchEffort=self.m.getReportWrenchEffort(self.qryWrench)

    # Generate one publisher and one topic for each component that is a sensor and uses post_message
    logger.info('######## PRIMITIVE DRIVER INITIALIZED ########')

def read_wrench(self, component_instance):
    """ Read the latest value from the Primitive Driver component
    """
    #curTime=self.current_MOOS_time
    parent_name = component_instance.robot_parent.blender_obj.name
    
    # read the most recent wrench effort command
    self.curWrenchEffort=elf.m.getReportWrenchEffort(self.qryWrench)

    # post to local_data for the actuator to pick up
    component_instance.local_data['v']=self.curWrenchEffort.getPropulsiveLinearEffortX_percent();
    component_instance.local_data['w']=self.curWrenchEffort.getPropulsiveRotationalEffortZ_percent();