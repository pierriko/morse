import GameLogic
import morse.core.robot
import PhysicsConstraints
import GameLogic
import mathutils
from morse.core.services import MorseServices

class SegwayRMP400Class(morse.core.robot.MorseRobotClass):
    """ Class definition for the Segway RMP400 base.
        Sub class of Morse_Object. """
              
    def __init__(self, obj, parent=None):
        """ Constructor method.
            Receives the reference to the Blender object.
            Optionally it gets the name of the object's parent,
            but that information is not currently used for a robot. """
        # Call the constructor of the parent class
        print ("######## ROBOT '%s' INITIALIZING ########" % obj.name)
        super(self.__class__,self).__init__(obj, parent)

        print ('######## ROBOT INITIALIZED ########')

    def default_action(self):
        """ Main function of this component. """
        pass

class SegwayRMP400VehicleClass(morse.core.robot.MorseVehicleRobotClass):
    """ Class definition for the Segway RMP400 base.
        Sub class of Morse_Object. """
              
    def __init__(self, obj, parent=None):
        """ Constructor method.
            Receives the reference to the Blender object.
            Optionally it gets the name of the object's parent,
            but that information is not currently used for a robot. """
        # Call the constructor of the parent class
        print ("######## ROBOT '%s' INITIALIZING ########" % obj.name)
        super(self.__class__,self).__init__(obj, parent)

        print ('######## ROBOT INITIALIZED ########')

    def default_action(self):
        """ Main function of this component. """
        pass


class SegwayRMP400PhysicsClass(morse.core.robot.MorsePhysicsRobotClass):
    """ Class definition for the Segway RMP400 base.
        Sub class of Morse_Object. """
              
    def __init__(self, obj, parent=None):
        """ Constructor method.
            Receives the reference to the Blender object.
            Optionally it gets the name of the object's parent,
            but that information is not currently used for a robot. """
        # Call the constructor of the parent class
        print ("######## ROBOT '%s' INITIALIZING ########" % obj.name)
        # define the wheel positions:
        self.wheelFLPos=mathutils.Vector((0.27, 0.312, 0.1))
        self.wheelFRPos=mathutils.Vector((0.27, -0.312, 0.1))
        self.wheelRLPos=mathutils.Vector((-0.27, 0.312, 0.1))
        self.wheelRRPos=mathutils.Vector((-0.27, -0.312, 0.1))
        
        super(self.__class__,self).__init__(obj, parent)

        print ('######## ROBOT INITIALIZED ########')

    def default_action(self):
        """ Main function of this component. """
        pass


