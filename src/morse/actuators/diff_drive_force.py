import GameLogic
import morse.core.actuator

class DiffDriveForceActuatorClass(morse.core.actuator.MorseActuatorClass):
    """ Motion controller using engine force on all wheels

    This class will read engine force for the wheels on each side 
    of a differential drive vehicle (force_l, force_r)
    as input from an external middleware, and then apply them
    to the parent robot.  Assumes the parent robot has four wheels
    with none of the wheels being steerable.
    """

    def __init__(self, obj, parent=None):
        print ('######## DIFF_DRIVE_FORCE CONTROL INITIALIZATION ########')
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        self.local_data['force_l'] = 400.0
        self.local_data['force_r'] = -400.0
        self.local_data['brake_l'] = 0.0
        self.local_data['brake_r'] = 0.0

        print ('######## CONTROL INITIALIZED ########')



    def default_action(self):
        """ Apply (steer, force) to the parent robot. """
        # Get the Blender object of the parent robot
        parent = self.robot_parent
        
        #Update the Force (speed) for these wheels:
        # TODO: only apply force to front wheels if vehicle is 4wd
        
        # assumes left wheels are 1 & 3 and right wheels are 0 & 2
        parent.local_data['vehicle'].applyEngineForce(self.local_data['force_l'],0)
        parent.local_data['vehicle'].applyEngineForce(self.local_data['force_l'],2)
        parent.local_data['vehicle'].applyEngineForce(self.local_data['force_r'],1)
        parent.local_data['vehicle'].applyEngineForce(self.local_data['force_r'],3)

        #Brakes:
        #Applies the braking force to each wheel listed:
        #['brakes'] = the game property value for the car labeled 'brakes'
        #Default value is 0:
        parent.local_data['vehicle'].applyBraking(self.local_data['brake_l'],0)
        parent.local_data['vehicle'].applyBraking(self.local_data['brake_l'],2)
        parent.local_data['vehicle'].applyBraking(self.local_data['brake_r'],1)
        parent.local_data['vehicle'].applyBraking(self.local_data['brake_r'],3)

