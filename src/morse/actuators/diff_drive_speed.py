import GameLogic
import morse.core.actuator

class SteerForceActuatorClass(morse.core.actuator.MorseActuatorClass):
    """ Motion controller using engine force and steer angle speeds

    This class will read engine force and steer angle (steer, force)
    as input from an external middleware, and then apply them
    to the parent robot.  Assumes the parent robot has four wheels
    with the front two being steerable.
    """

    def __init__(self, obj, parent=None):
        print ('######## STEER_FORCE CONTROL INITIALIZATION ########')
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        self.local_data['v_l'] = 0.0    # left side wheel speed
        self.local_data['v_r'] = 0.0    # right side wheel speed
        
        # find the wheels and add actuators to them
        
        
        
        # Choose the type of function to move the object
        #self._type = 'Velocity'
        #self._type = 'Position'

        print ('######## CONTROL INITIALIZED ########')



    def default_action(self):
        """ Apply (steer, force) to the parent robot. """
        # Get the Blender object of the parent robot
        parent = self.robot_parent
        
        # update the wheel velocities
        
        
        #Update the steering value for these wheels:
        #The number the end represents the wheel 'number' in the 
        #order they were created above.  Front wheels #0 and #1.
        #Rear wheels #2 and #3.
        parent.vehicle.setSteeringValue(self.local_data['steer'],0)
        parent.vehicle.setSteeringValue(self.local_data['steer'],1)

