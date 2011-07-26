import GameLogic
import morse.core.robot
#import bge.constraints
#import bge.logic
import PhysicsConstraints
import bge
import math

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

        # determines if vehicle has suspension or just wheels
        self.hasSuspension=False

        # get pointers to and physicsIds of all objects
        # get wheel pointers - needed by wheel speed sensors
        self.local_data['wheelFL']=scene.objects['rmp_wheel_atv.000']
        self.local_data['wheelFR']=scene.objects['rmp_wheel_atv.001']
        self.local_data['wheelRL']=scene.objects['rmp_wheel_atv.002']
        self.local_data['wheelRR']=scene.objects['rmp_wheel_atv.003']
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
        
        # try to lock a wheel
        #wheelFLJoint.setParam(3,0.0,0.0) # no rotation about Y axis
        
        # unlock wheel
        #wheelFLJoint.setParam(3,-10000.0,10000.0) # no rotation about Y axis
        
        #wheelFLJoint.setParam(9,0.0,10000.0)
        #wheelFRJoint.setParam(9,0.0,10000.0)
        #wheelRLJoint.setParam(9,0.0,10000.0)
        #wheelRRJoint.setParam(9,0.0,10000.0)
        
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
        
        
    # TODO: these functions should be put in a separate module later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def GetRelativePos (self, obj_c,obj_p):
        # could i do this better by just subtracting positions?
        obj_c.setParent(obj_p)
        pos = obj_c.localPosition
        obj_c.removeParent()
        return pos    
        
    def AttachWheelToBody(self, wheel, parent):
        #wheelPos=self.GetRelativePos(wheel, parent)
        result = parent.getVectTo(wheel);
        wheelPos=result[0]*result[2]
        print(result)
        print(wheelPos)
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
