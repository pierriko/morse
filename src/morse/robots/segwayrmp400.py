import GameLogic
import morse.core.robot
#import bge.constraints
#import bge.logic
import PhysicsConstraints
import bpy
import math
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
        
        # get a link to the blender scene to look for wheel and suspension objects
        scene = GameLogic.getCurrentScene()
        
        # determines if vehicle has suspension or just wheels
        self.hasSuspension=self.blender_obj['HasSuspension']

        # get pointers to and physicsIds of all objects
        # get wheel pointers - needed by wheel speed sensors
        self.local_data['wheelFL']=scene.objects[self.blender_obj['WheelFLName']]
        self.local_data['wheelFR']=scene.objects[self.blender_obj['WheelFRName']]
        self.local_data['wheelRL']=scene.objects[self.blender_obj['WheelRLName']]
        self.local_data['wheelRR']=scene.objects[self.blender_obj['WheelRRName']]
        self.local_data['numWheels']=4
         # wheel ID's
        self.local_data['wheelFL_ID'] = self.local_data['wheelFL'].getPhysicsId()
        self.local_data['wheelFR_ID'] = self.local_data['wheelFR'].getPhysicsId()
        self.local_data['wheelRL_ID'] = self.local_data['wheelRL'].getPhysicsId()
        self.local_data['wheelRR_ID'] = self.local_data['wheelRR'].getPhysicsId()
        # body ID
        chassis_ID = self.blender_obj.getPhysicsId()
        # suspension arm ID's
        
        # set up wheel constraints
        # add wheels to either suspension arms or vehicle chassis
        if (self.hasSuspension):
            # TODO: ADD THESE LATER!!!!!!!!!!
            pass
        else:
            # get relative positions between wheels and chassis
            self.local_data['wheelFLJoint']=self.AttachWheelToBody(self.local_data['wheelFL'],self.blender_obj)  
            self.local_data['wheelFRJoint']=self.AttachWheelToBody(self.local_data['wheelFR'],self.blender_obj) 
            self.local_data['wheelRLJoint']=self.AttachWheelToBody(self.local_data['wheelRL'],self.blender_obj) 
            self.local_data['wheelRRJoint']=self.AttachWheelToBody(self.local_data['wheelRR'],self.blender_obj) 
            #pass
            
        # get wheel radius
        self.local_data['wheelRadius']=0.27  # TODO read this later from GameObjectSettings.radius

        # get track width
        posL=self.local_data['wheelRL'].position
        posR=self.local_data['wheelRR'].position
        # subtract y coordinates of wheels to get width
        self.local_data['trackWidth']=posL[1]-posR[1]

        print ('######## ROBOT INITIALIZED ########')

    def getWheelSpeeds(self):
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wsFL=self.local_data['wheelFL'].getAngularVelocity(True)
        wsFR=self.local_data['wheelFR'].getAngularVelocity(True)
        wsRL=self.local_data['wheelRL'].getAngularVelocity(True)
        wsRR=self.local_data['wheelRR'].getAngularVelocity(True)
        return [wsFL[2], wsFR[2], wsRL[2], wsRR[2]]
        
    def getWheelAngle(self):
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wcFL=self.local_data['wheelFL'].localOrientation.to_euler()
        #print(wcFL)
        wcFR=self.local_data['wheelFR'].localOrientation.to_euler()
        wcRL=self.local_data['wheelRL'].localOrientation.to_euler()
        wcRR=self.local_data['wheelRR'].localOrientation.to_euler()
        return [wcFL[1], wcFR[1], wcRL[1], wcRR[1]]

    def default_action(self):
        """ Main function of this component. """
        pass
        #self.getWheelCount()

    # TODO: these functions should be put in a separate module later or
    # a new robot class created
        
    def AttachWheelToBody(self, wheel, parent):
        #wheelPos=self.GetRelativePos(wheel, parent)
        result = parent.getVectTo(wheel);
        wheelPos=result[0]*result[2]
        joint = PhysicsConstraints.createConstraint( parent.getPhysicsId(),
                                     wheel.getPhysicsId(),
                                     12,    # 6dof constraint
                                     wheelPos[0], wheelPos[1], wheelPos[2],  # pivot position
                                     0,0,0,     # pivot axis
                                     128) # flag, 128=disable collision between wheel and parent
        # no parameters are set on x axis to allow full rotation about it
        joint.setParam(4,0.0,0.0) # no rotation about Y axis
        joint.setParam(5,0.0,0.0) # no rotation about Z axis
        return joint
    
    
    def AttachWheelWithSuspension(self, wheel, parent, suspensionArm):
        pass
