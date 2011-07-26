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

        self.local_data['wheelFL']=scene.objects['rmp_wheel_atv.000']
        self.local_data['wheelFR']=scene.objects['rmp_wheel_atv.001']
        self.local_data['wheelRL']=scene.objects['rmp_wheel_atv.002']
        self.local_data['wheelRR']=scene.objects['rmp_wheel_atv.003']
        self.local_data['numWheels']=4
        
        # get wheel radius
        self.local_data['wheelRadius']=0.27  # TODO read this later from GameObjectSettings.radius
       
        print(self.local_data['wheelRR'].parent)
        print(self.local_data['wheelRR'].getPhysicsId())
        
        
        # get track width
        posL=self.local_data['wheelRL'].position
        posR=self.local_data['wheelRR'].position
        # subtract y coordinates of wheels to get width
        self.local_data['trackWidth']=posL[1]-posR[1]
        print(self.local_data['trackWidth'])

        # true parameters tell it velocities are local
        self.local_data['wheelFL'].setAngularVelocity([0.0,0.0,0.0],True)
        self.local_data['wheelFR'].setAngularVelocity([0.0,0.0,0.0],True)
        self.local_data['wheelRL'].setAngularVelocity([0.0,0.0,0.0],True)
        self.local_data['wheelRR'].setAngularVelocity([0.0,0.0,0.0],True)

        print ('######## ROBOT INITIALIZED ########')

    def getWheelSpeeds(self):
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wsFL=self.local_data['wheelFL'].getAngularVelocity(True)
        wsFR=self.local_data['wheelFR'].getAngularVelocity(True)
        wsRL=self.local_data['wheelRL'].getAngularVelocity(True)
        wsRR=self.local_data['wheelRR'].getAngularVelocity(True)
        return [wsFL[2], wsFR[2], wsRL[2], wsRR[2]]
        

    def default_action(self):
        """ Main function of this component. """
        pass
        
        #self.local_data['wheelFL'].setAngularVelocity([0.0,0.0,2.0],True)
        #self.local_data['wheelFR'].setAngularVelocity([0.0,0.0,-2.0],True)
        #self.local_data['wheelRL'].setAngularVelocity([0.0,0.0,2.0],True)
        #self.local_data['wheelRR'].setAngularVelocity([0.0,0.0,-2.0],True)
