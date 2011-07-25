import GameLogic
import morse.core.robot
import PhysicsConstraints
import bge

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
        
        scene = GameLogic.getCurrentScene()
        #print(dir(scene))
        #print(dir(scene.objects))
        #print(dir(scene.objects['rmp_wheel_atv.000']))

        wheel1=scene.objects['rmp_wheel_atv.000']
        wheel2=scene.objects['rmp_wheel_atv.001']
        wheel3=scene.objects['rmp_wheel_atv.002']
        wheel4=scene.objects['rmp_wheel_atv.003']

        wheel1.setAngularVelocity([0.0,0.0,5.0],True)
        wheel2.setAngularVelocity([0.0,0.0,-5.0],True)
        wheel3.setAngularVelocity([0.0,0.0,5.0],True)
        wheel4.setAngularVelocity([0.0,0.0,-5.0],True)

        print ('######## ROBOT INITIALIZED ########')

    def default_action(self):
        """ Main function of this component. """
        pass
