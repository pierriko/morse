import logging; logger = logging.getLogger("morse." + __name__)
from abc import ABCMeta
import morse.core.object
import math
import bge
import bpy

class MorseRobotClass(morse.core.object.MorseObjectClass):
    """ Basic Class for all robots

    Inherits from the base object class.
    """

    # Make this an abstract class
    __metaclass__ = ABCMeta

    def __init__ (self, obj, parent=None):
        """ Constructor method. """
        # Call the constructor of the parent class
        super(MorseRobotClass, self).__init__(obj, parent)
        
        # Add the variable move_status to the object
        self.move_status = "Stop"
        logger.setLevel(logging.DEBUG)

    def action(self):
        """ Call the regular action function of the component. """
        # Update the component's position in the world
        self.position_3d.update(self.blender_obj)

        self.default_action()

class FourWheelRobotClass(MorseRobotClass): 

    # Make this an abstract class
    __metaclass__ = ABCMeta
       
    def GetWheels(self):
        # get pointers to and physicsIds of all objects
        # get wheel pointers - needed by wheel speed sensors and to
        # set up constraints
        # bullet vehicles always have 4 wheels
        scene=bge.logic.getCurrentScene()
        self.numWheels=4  
        
        # front left wheel
        try:
            self._wheelFL=scene.objects[self.blender_obj['WheelFLName']]
        except:
            import traceback
            traceback.print_exc()         
          

        # front right wheel
        try:
            self._wheelFR=scene.objects[self.blender_obj['WheelFRName']]
        except:
            import traceback
            traceback.print_exc() 

        # rear left wheel
        try:
            self._wheelRL=scene.objects[self.blender_obj['WheelRLName']]
        except:
            import traceback
            traceback.print_exc()         
 
        # rear right wheel
        try:
            self._wheelRR=scene.objects[self.blender_obj['WheelRRName']]
        except:
            import traceback
            traceback.print_exc()          

        # make sure wheels are not children of the robot
        if (bpy.data.objects[self.blender_obj['WheelFLName']].parent is not None):
            #bpy.ops.object.select_name(name=self.blender_obj['WheelFLName'])
            #bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            self._wheelFL.removeParent()
            #self.local_data['wheelFL'].enableRigidBody()
            
        if (bpy.data.objects[self.blender_obj['WheelFRName']].parent is not None):    
            #bpy.ops.object.select_name(name=self.blender_obj['WheelFRName'])
            #bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            self._wheelFR.removeParent()
            #self.local_data['wheelFR'].enableRigidBody()

        if (bpy.data.objects[self.blender_obj['WheelRLName']].parent is not None):
            #bpy.ops.object.select_name(name=self.blender_obj['WheelRLName'])
            #bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            self._wheelRL.removeParent()
            #self.local_data['wheelRL'].enableRigidBody()
            
        if (bpy.data.objects[self.blender_obj['WheelRRName']].parent is not None):
            #bpy.ops.object.select_name(name=self.blender_obj['WheelRRName'])
            #bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            self._wheelRR.removeParent()
            #self.local_data['wheelRR'].enableRigidBody()

        # DEBUG: check mass to see if physics controller is enabled
        #print(self._wheelFL.mass)
        #print(self._wheelFR.mass)
        #print(self._wheelRL.mass)
        #print(self._wheelRR.mass)

        #import pdb
        #pdb.set_trace()

        # get wheel radius
        self._wheelRadius=self.GetWheelRadius(self.blender_obj['WheelFLName'])


    def ReadGenericParameters(self):
        # get needed parameters from the blender object
        # determines if vehicle has suspension or just wheels
        try:
            self._HasSuspension=self.blender_obj['HasSuspension']
        except KeyError as e:
            self._HasSuspension=True
            logger.info('HasSuspension property not present and defaulted to True')
        except:
            import traceback
            traceback.print_exc() 

        # determines if vehicle has steerable front wheels or not
        try:
            self._HasSteering=self.blender_obj['HasSteering']
        except KeyError as e:
            self._HasSteering=True
            logger.info('HasSteering property not present and defaulted to True')
        except:
            import traceback
            traceback.print_exc() 
        
    def GetTrackWidth(self):
        # get lateral positions of the wheels
        posL=self._wheelFL.position
        posR=self._wheelFR.position
        # subtract y coordinates of wheels to get width
        return posL[1]-posR[1]

    def GetWheelRadius(self, wheelName):
        dims=bpy.data.objects[wheelName].dimensions
        # average the x and y dimension to get diameter - divide by 2 for radius
        return (dims[0]+dims[1])/4

class MorseVehicleRobotClass(FourWheelRobotClass):
    """ Basic Class for robots using the Bullet vehicle constraint

    Inherits from the base robot class.
    """

    def __init__ (self, obj, parent=None):
        """ Constructor method. """
        # Call the constructor of the parent class
        super(MorseVehicleRobotClass, self).__init__(obj, parent)
    
        # construct the vehicle
        self.build_vehicle()

    def build_vehicle(self):
        """ Apply the constraints to the vehicle parts. """
        #import pdb; pdb.set_trace()
        # get the physics ID of the chassis to create constraint with
        self._chassisId = self.blender_obj.getPhysicsId()
        # set up bullet vehicle constraint - constraint type 11 = bullet vehicle
        vehicle=PhysicsConstraints.createConstraint(self._chassisId,0,11)
        cid=vehicle.getConstraintId()
        # store vehicle constraint so actuators and sensors 
        self._vehicle = PhysicsConstraints.getVehicleConstraint(cid)
            
        # read the needed parameters from the blender object properties
        self.ReadGenericParameters()
        self.ReadParameters()
        # get references to all of the wheels
        self.GetWheels() 

        # get physics ID's of wheels
        self._wheelFL_ID = self._wheelFL.getPhysicsId()
        self._wheelFR_ID = self._wheelFR.getPhysicsId()
        self._wheelRL_ID = self._wheelRL.getPhysicsId()
        self._wheelRR_ID = self._wheelRR.getPhysicsId()
 
        
        # get track width
        self._trackWidth=self.GetTrackWidth();
        
        # add wheels
        # front wheels - steerable if property is true
        self.AttachWheelToBody(self._wheelFL, self.blender_obj, self._HasSteering)
        self.AttachWheelToBody(self._wheelFR, self.blender_obj, self._HasSteering)
        # rear wheels - never steerable
        self.AttachWheelToBody(self._wheelRL, self.blender_obj, False)
        self.AttachWheelToBody(self._wheelRR, self.blender_obj, False)
            
        # set properties - see doc for meaning
        self._vehicle.setRollInfluence(self._influence,0)
        self._vehicle.setRollInfluence(self._influence,1)
        self._vehicle.setRollInfluence(self._influence,2)
        self._vehicle.setRollInfluence(self._influence,3)        

        self._vehicle.setSuspensionStiffness(self._stiffness,0)
        self._vehicle.setSuspensionStiffness(self._stiffness,1)
        self._vehicle.setSuspensionStiffness(self._stiffness,2)
        self._vehicle.setSuspensionStiffness(self._stiffness,3)

        self._vehicle.setSuspensionDamping(self._damping,0)
        self._vehicle.setSuspensionDamping(self._damping,1)
        self._vehicle.setSuspensionDamping(self._damping,2)
        self._vehicle.setSuspensionDamping(self._damping,3)

        self._vehicle.setSuspensionCompression(self._compression,0)
        self._vehicle.setSuspensionCompression(self._compression,1)
        self._vehicle.setSuspensionCompression(self._compression,2)
        self._vehicle.setSuspensionCompression(self._compression,3)

        self._vehicle.setTyreFriction(self._friction,0)
        self._vehicle.setTyreFriction(self._friction,1)
        self._vehicle.setTyreFriction(self._friction,2)
        self._vehicle.setTyreFriction(self._friction,3)

    def AttachWheelToBody(self, wheel, parent,hasSteering):
        """ Attaches the wheel to the given parent using a 6DOF constraint """
        #wheelAttachDirLocal:
        #Direction the suspension is pointing
        wheelAttachDirLocal = [0,0,-1]
        #wheelAxleLocal:
        #Determines the rotational angle where the
        #wheel is mounted.
        wheelAxleLocal = [-1,0,0]
        
        #wheelAttachPosLocal:
        #Where the wheel is attach to the car based
        #on the vehicle's center
        result = parent.getVectTo(wheel);
        # result is a unit vector (result[2]) and a length(result[0])
        # multiply them together to get the complete vector
        wheelPos=result[0]*result[2]  
        joint=self._vehicle.addWheel(wheel,wheelPos,wheelAttachDirLocal,wheelAxleLocal,self._suspensionRestLength,self._wheelRadius,hasSteering)
 
        return joint # return a reference to the constraint

    def ReadParameters(self):
        """ Read needed parameters from the Blender object """
                
        # get needed parameters from the blender object
        # determines if vehicle has suspension or just wheels
          
        # only read these properties if there is a suspension
        if self._HasSuspension:    
            try:
                self._suspensionRestLength=self.blender_obj['SuspensionRestLength']
            except KeyError as e:
                self._suspensionRestLength=0.3
                logger.info('SuspensionRestLength property not present and defaulted to 0.3m')
            except:
                import traceback
                traceback.print_exc() 
            

            #Stiffness:
            #Affects how quickly the suspension will 'spring back'
            #0 = No Spring back
            # .001 and higher = faster spring back
            try:
                self._stiffness=self.blender_obj['Stiffness']
            except KeyError as e:
                self._stiffness=25.0
                logger.info('Stiffness property not present and defaulted to 25.0')
            except:
                import traceback
                traceback.print_exc() 
            
            
            #Dampening:
            #Determines how much the suspension will absorb the
            #compression.
            #0 = Bounce like a super ball
            #greater than 0 = less bounce
            try:
                self._damping=self.blender_obj['Damping']
            except KeyError as e:
                self._damping=10.0
                logger.info('Damping property not present and defaulted to 10.0')
            except:
                import traceback
                traceback.print_exc() 


            
            #Compression:
            #Resistance to compression of the overall suspension length.
            #0 = Compress the entire length of the suspension
            #Greater than 0 = compress less than the entire suspension length.
            #10 = almost no compression
            try:
                self._compression=self.blender_obj['Compression']
            except KeyError as e:
                self._compression=2.0
                logger.info('Compression property not present and defaulted to 2.0')
            except:
                import traceback
                traceback.print_exc()  
        else:  # no suspension
            self._compression=10.0 # no compression
            self._damping=10000.0 # no bouncing
            self._stiffness=10.0 # maximum stiffness
            self._suspensionRestLength=0.0


        # read these properties whether there is a suspension or not

        #The Rolling Influence:
        #How easy it will be for the vehicle to roll over while turning:
        #0 = Little to no rolling over
        # .1 and higher easier to roll over
        #Wheels that loose contact with the ground will be unable to
        #steer the vehicle as well.
        try:
            if self.blender_obj['Influence']:
                self._influence=self.blender_obj['Influence']
        except KeyError as e:
            self._influence=0.075
            logger.info('Influence property not present and defaulted to 0.075')
        except:
            import traceback
            traceback.print_exc() 

        # TODO: try to get friction from the wheel material
        #Friction:
        #Wheel's friction to the ground
        #How fast you can accelerate from a standstill.
        #Also affects steering wheel's ability to turn vehicle.
        #0 = Very Slow Acceleration:
        # .1 and higher = Faster Acceleration / more friction:
        try:
            if self.blender_obj['Friction']:
                self._friction=self.blender_obj['Friction']
        except KeyError as e:
            self._friction=0.8
            logger.info('Friction property not present and defaulted to 0.8')
        except:
            import traceback
            traceback.print_exc()         

    def getWheelSpeeds(self):
        """ Returns the angular wheel velocity in rad/sec"""
        return (0.0,0.0,0.0,0.0)
        
    def getWheelAngle(self):
        """ Returns the accumulated wheel angle in radians"""
        angFL=self._vehicle.getWheelOrientationQuaternion(0).to_euler()[0]
        angFR=self._vehicle.getWheelOrientationQuaternion(1).to_euler()[0]
        angRL=self._vehicle.getWheelOrientationQuaternion(2).to_euler()[0]
        angRR=self._vehicle.getWheelOrientationQuaternion(3).to_euler()[0]
        return (angFL,angFR,angRL,angRR)

    def GetWheelRadius(self, wheelName):
        dims=bpy.data.objects[wheelName].dimensions
        # average the y and z dimension to get diameter - divide by 2 for radius
        return (dims[1]+dims[2])/4
    
class MorsePhysicsRobotClass(FourWheelRobotClass):
    """ Basic Class for robots using individual physics constraints

    Inherits from the base robot class.
    """

    def __init__ (self, obj, parent=None):
        """ Constructor method. """
        
        # Call the constructor of the parent class
        super(MorsePhysicsRobotClass, self).__init__(obj, parent)
        
        # construct the vehicle
        self.build_vehicle()

    def build_vehicle(self):
        """ Apply the constraints to the vehicle parts. """
        
        # get a link to the blender scene to look for wheel and suspension objectsscene = GameLogic.getCurrentScene()
        # get needed parameters from the blender object
        self.ReadGenericParameters()
        
        # chassis ID - main object should be chassis model
        self._chassis_ID = self.blender_obj.getPhysicsId()
        # get wheel references and ID's
        self.GetWheels()

        # get track width
        self._trackWidth=self.GetTrackWidth();

        # set up wheel constraints
        # add wheels to either suspension arms or vehicle chassis
        if (self._HasSuspension):
            self.BuildModelWithSuspension()
        else:
            self.BuildModelWithoutSuspension()

    def BuildModelWithSuspension(self):
        """ Add all the constraints to attach the wheels to 
        the a-arms and then the a-arms to the body """
        scene = GameLogic.getCurrentScene()
        # get suspension arm ID's
        # front left A-arm
        try:
            if self.blender_obj['ArmFLName']:
                self._armFL=scene.objects[self.blender_obj['ArmFLName']]
        except:
            import traceback
            traceback.print_exc()         
 
        # front right A-arm
        try:
            if self.blender_obj['ArmFRName']:
                self._armFR=scene.objects[self.blender_obj['ArmFRName']]
        except:
            import traceback
            traceback.print_exc()          
 

        # rear left arm
        try:
            if self.blender_obj['ArmRLName']:
                self._armRL=self.blender_obj['ArmRLName']
        except:
            import traceback
            traceback.print_exc()   

        # rear right arm
        try:
            if self.blender_obj['ArmRRName']:
                self._armRR=self.blender_obj['ArmRRName']
        except:
            import traceback
            traceback.print_exc()  
        
        # put together front wheels and suspension
        self._wheelFLJoint=self.AttachWheelWithSuspension(self._wheelFL,self.blender_obj,self._armFL)  
        self._wheelFRJoint=self.AttachWheelWithSuspension(self._wheelFR,self.blender_obj,self._armFR) 
            
        self._wheelRLJoint=self.AttachWheelWithSuspension(self._wheelRL,self.blender_obj,self._armRL)  
        self._wheelRRJoint=self.AttachWheelWithSuspension(self._wheelRR,self.blender_obj,self._armRR) 

    def BuildModelWithoutSuspension(self):
        """ Add all the constraints to attach the wheels to the body """
        # add front wheels
        self._wheelFLJoint=self.AttachWheelToBody(self._wheelFL,self.blender_obj, self._wheelFLPos)  
        self._wheelFRJoint=self.AttachWheelToBody(self._wheelFR,self.blender_obj, self._wheelFRPos) 
        # add rear wheels 
        self._wheelRLJoint=self.AttachWheelToBody(self._wheelRL,self.blender_obj, self._wheelRLPos) 
        self._wheelRRJoint=self.AttachWheelToBody(self._wheelRR,self.blender_obj, self._wheelRRPos) 

    def AttachWheelToBody(self, wheel, parent, wheelPos):
        """ Attaches the wheel to the given parent using a 6DOF constraint """
        # set the wheel positions relative to the robot in case the
        # chassis was moved by the builder script or manually in blender
        #import pdb
        #pdb.set_trace()
        globalWheelPos=wheelPos+parent.worldPosition
        wheel.worldPosition=globalWheelPos
        
        # get the new relative position and use it for the constraints
        result = parent.getVectTo(wheel);
        ## result is a unit vector (result[2]) and a length(result[0])
        ## multiply them together to get the complete vector
        wheelPos=result[0]*result[2]        

        logger.debug("Added wheel '%s' at ('%f','%f','%f')" %(wheel.name, wheelPos[0], wheelPos[1], wheelPos[2]))

        # create constraint to allow wheel to spin
        joint = bge.constraints.createConstraint( parent.getPhysicsId(),  # get physics ID of the parent object
                                     wheel.getPhysicsId(),  # get physics ID of the wheel object
                                     12,    # 6dof constraint
                                     wheelPos[0], wheelPos[1], wheelPos[2],  # pivot position
                                     0,0,0,     # pivot axis
                                     128) # flag, 128=disable collision between wheel and parent
        # no parameters are set on x axis to allow full rotation about it
        joint.setParam(4,0.0,0.0) # no rotation about Y axis - min=0, max=0
        joint.setParam(5,0.0,0.0) # no rotation about Z axis - min=0, max=0
        return joint # return a reference to the constraint
        
    def AttachWheelWithSuspension(self, wheel, parent, suspensionArm):
        """ Attaches the wheel to the a-arm and then the a-arm to the body """
        # TODO: fill this in later - model after Bueraki code
        pass

    def getWheelSpeeds(self):
        """ Returns the angular wheel velocity in rad/sec"""
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wsFL=self._wheelFL.getAngularVelocity(True)
        wsFR=self._wheelFR.getAngularVelocity(True)
        wsRL=self._wheelRL.getAngularVelocity(True)
        wsRR=self._wheelRR.getAngularVelocity(True)
        return [wsFL[2], wsFR[2], wsRL[2], wsRR[2]]

    def getWheelAngle(self):
        """ Returns the accumulated wheel angle in radians"""
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wcFL=self._wheelFL.localOrientation.to_euler()
        wcFR=self._wheelFR.localOrientation.to_euler()
        wcRL=self._wheelRL.localOrientation.to_euler()
        wcRR=self._wheelRR.localOrientation.to_euler()
        return [wcFL[1], wcFR[1], wcRL[1], wcRR[1]]

    def AttachWheelToWheel(self,wheel1,wheel2):
        # add both wheels on each side to each other but with no
        # constraints on their motion so that no collision can be set
        # between them
        pass
    
