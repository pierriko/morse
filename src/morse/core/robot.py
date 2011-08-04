import logging; logger = logging.getLogger("morse." + __name__)
from abc import ABCMeta
import morse.core.object
import math
import PhysicsConstraints
import GameLogic
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
        scene=GameLogic.getCurrentScene()
        self.local_data['numWheels']=4  
        
        # front left wheel
        try:
            self.local_data['wheelFL']=scene.objects[self.blender_obj['WheelFLName']]
        except:
            import traceback
            traceback.print_exc()         
 
        # front right wheel
        try:
            self.local_data['wheelFR']=scene.objects[self.blender_obj['WheelFRName']]
        except:
            import traceback
            traceback.print_exc() 
        
        # rear left wheel
        try:
            self.local_data['wheelRL']=scene.objects[self.blender_obj['WheelRLName']]
        except:
            import traceback
            traceback.print_exc()         
 
        # rear right wheel
        try:
            self.local_data['wheelRR']=scene.objects[self.blender_obj['WheelRRName']]
        except:
            import traceback
            traceback.print_exc()          

        def GetWheels(self):
            # get track width
            posL=self.local_data['wheelFL'].position
            posR=self.local_data['wheelFR'].position
            # subtract y coordinates of wheels to get width
            return posL[1]-posR[1]

    def GetWheelRadius(self, wheelName):
        #import pdb
        #pdb.set_trace()
        dims=bpy.data.objects[wheelName].dimensions
        # average the x and y dimension to get diameter - divide by 2 for radius
        return (dims[1]+dims[2])/4

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
        posL=self.local_data['wheelFL'].position
        posR=self.local_data['wheelFR'].position
        # subtract y coordinates of wheels to get width
        return posL[1]-posR[1]

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
        # get the physics ID of the chassis to create constraint with
        self._chassisId = self.blender_obj.getPhysicsId()
        # set up bullet vehicle constraint - constraint type 11 = bullet vehicle
        vehicle=PhysicsConstraints.createConstraint(self._chassisId,0,11)
        cid=vehicle.getConstraintId()
        # store vehicle constraint so actuators and sensors 
        self.local_data['vehicle'] = PhysicsConstraints.getVehicleConstraint(cid)
            
        # read the needed parameters from the blender object properties
        self.ReadGenericParameters()
        self.ReadParameters()
        # get references to all of the wheels
        self.GetWheels()    
        
        # get track width
        self.local_data['trackWidth']=self.GetTrackWidth();
        
        # add wheels
        # front wheels - steerable if property is true
        self.AttachWheelToBody(self.local_data['wheelFL'], self._HasSteering)
        self.AttachWheelToBody(self.local_data['wheelFR'], self._HasSteering)
        # rear wheels - never steerable
        self.AttachWheelToBody(self.local_data['wheelRL'], False)
        self.AttachWheelToBody(self.local_data['wheelRR'], False)
            
        # set properties - see doc for meaning
        self.local_data['vehicle'].setRollInfluence(self._Influence,0)
        self.local_data['vehicle'].setRollInfluence(self._Influence,1)
        self.local_data['vehicle'].setRollInfluence(self._Influence,2)
        self.local_data['vehicle'].setRollInfluence(self._Influence,3)        

        self.local_data['vehicle'].setSuspensionStiffness(self._Stiffness,0)
        self.local_data['vehicle'].setSuspensionStiffness(self._Stiffness,1)
        self.local_data['vehicle'].setSuspensionStiffness(self._Stiffness,2)
        self.local_data['vehicle'].setSuspensionStiffness(self._Stiffness,3)

        self.local_data['vehicle'].setSuspensionDamping(self._Damping,0)
        self.local_data['vehicle'].setSuspensionDamping(self._Damping,1)
        self.local_data['vehicle'].setSuspensionDamping(self._Damping,2)
        self.local_data['vehicle'].setSuspensionDamping(self._Damping,3)

        self.local_data['vehicle'].setSuspensionCompression(self._Compression,0)
        self.local_data['vehicle'].setSuspensionCompression(self._Compression,1)
        self.local_data['vehicle'].setSuspensionCompression(self._Compression,2)
        self.local_data['vehicle'].setSuspensionCompression(self._Compression,3)

        self.local_data['vehicle'].setTyreFriction(self._Friction,0)
        self.local_data['vehicle'].setTyreFriction(self._Friction,1)
        self.local_data['vehicle'].setTyreFriction(self._Friction,2)
        self.local_data['vehicle'].setTyreFriction(self._Friction,3)

    def AttachWheelToBody(self, wheel, hasSteering):
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
        # get relative position between the wheel and the parent from the model
        result = self.blender_obj.getVectTo(wheel);
        # result is a unit vector (result[2]) and a length(result[0])
        # multiply them together to get the complete vector
        wheelAttachPosLocal=result[0]*result[2]
        joint=self.local_data['vehicle'].addWheel(wheel,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,self._SuspensionRestLength,self.local_data['WheelRadius'],hasSteering)
 
        return joint # return a reference to the constraint

    def ReadParameters(self):
        """ Read needed parameters from the Blender object """
                
        # get needed parameters from the blender object
        # determines if vehicle has suspension or just wheels
          
        # only read these properties if there is a suspension
        if self._HasSuspension:    
            try:
                self._SuspensionRestLength=self.blender_obj['SuspensionRestLength']
            except KeyError as e:
                self._SuspensionRestLength=0.3
                logger.info('SuspensionRestLength property not present and defaulted to 0.3m')
            except:
                import traceback
                traceback.print_exc() 
            

            #Stiffness:
            #Affects how quickly the suspension will 'spring back'
            #0 = No Spring back
            # .001 and higher = faster spring back
            try:
                self._Stiffness=self.blender_obj['Stiffness']
            except KeyError as e:
                self._Stiffness=25.0
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
                self._Damping=self.blender_obj['Damping']
            except KeyError as e:
                self._Damping=10.0
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
                self._Compression=self.blender_obj['Compression']
            except KeyError as e:
                self._Compression=2.0
                logger.info('Compression property not present and defaulted to 2.0')
            except:
                import traceback
                traceback.print_exc()  
        else:  # no suspension
            self._Compression=10.0 # no compression
            self._Damping=10000.0 # no bouncing
            self._Stiffness=10.0 # maximum stiffness
            self._SuspensionRestLength=0.0


        # read these properties whether there is a suspension or not

        #The Rolling Influence:
        #How easy it will be for the vehicle to roll over while turning:
        #0 = Little to no rolling over
        # .1 and higher easier to roll over
        #Wheels that loose contact with the ground will be unable to
        #steer the vehicle as well.
        try:
            if self.blender_obj['Influence']:
                self._Influence=self.blender_obj['Influence']
        except KeyError as e:
            self._Influence=0.075
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
                self._Friction=self.blender_obj['Friction']
        except KeyError as e:
            self._Friction=0.8
            logger.info('Friction property not present and defaulted to 0.8')
        except:
            import traceback
            traceback.print_exc()         

    def getWheelSpeeds(self):
        """ Returns the angular wheel velocity in rad/sec"""
        return (0.0,0.0,0.0,0.0)
        
    def getWheelAngle(self):
        """ Returns the accumulated wheel angle in radians"""
        return (0.0,0.0,0.0,0.0)

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

        self.local_data['WheelRadius']=self.GetWheelRadius(self.blender_obj['WheelFLName'])

        # get track width
        self.local_data['trackWidth']=self.GetTrackWidth();

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
                self.local_data['armFL']=scene.objects[self.blender_obj['ArmFLName']]
        except:
            import traceback
            traceback.print_exc()         
 
        # front right A-arm
        try:
            if self.blender_obj['ArmFRName']:
                self.local_data['armFR']=scene.objects[self.blender_obj['ArmFRName']]
        except:
            import traceback
            traceback.print_exc()          
 

        # rear left arm
        try:
            if self.blender_obj['ArmRLName']:
                self.local_data['armRL']=self.blender_obj['ArmRLName']
        except:
            import traceback
            traceback.print_exc()   

        # rear right arm
        try:
            if self.blender_obj['ArmRRName']:
                self.local_data['armRR']=self.blender_obj['ArmRRName']
        except:
            import traceback
            traceback.print_exc()  
        
        # put together front wheels and suspension
        self.local_data['wheelFLJoint']=self.AttachWheelWithSuspension(self.local_data['wheelFL'],self.blender_obj,self.local_data['armFL'])  
        self.local_data['wheelFRJoint']=self.AttachWheelWithSuspension(self.local_data['wheelFR'],self.blender_obj,self.local_data['armFR']) 
            
        self.local_data['wheelRLJoint']=self.AttachWheelWithSuspension(self.local_data['wheelRL'],self.blender_obj,self.local_data['armRL'])  
        self.local_data['wheelRRJoint']=self.AttachWheelWithSuspension(self.local_data['wheelRR'],self.blender_obj,self.local_data['armRR']) 

    def BuildModelWithoutSuspension(self):
        """ Add all the constraints to attach the wheels to the body """
        # make joints available to actuator so force or torque can be applied
        # add front wheels
        self.local_data['wheelFLJoint']=self.AttachWheelToBody(self.local_data['wheelFL'],self.blender_obj)  
        self.local_data['wheelFRJoint']=self.AttachWheelToBody(self.local_data['wheelFR'],self.blender_obj) 
        # add rear wheels 
        self.local_data['wheelRLJoint']=self.AttachWheelToBody(self.local_data['wheelRL'],self.blender_obj) 
        self.local_data['wheelRRJoint']=self.AttachWheelToBody(self.local_data['wheelRR'],self.blender_obj) 

    def AttachWheelToBody(self, wheel, parent):
        """ Attaches the wheel to the given parent using a 6DOF constraint """
        # get relative position between the wheel and the parent from the model
        result = parent.getVectTo(wheel);
        # result is a unit vector (result[2]) and a length(result[0])
        # multiply them together to get the complete vector
        wheelPos=result[0]*result[2]
        # create a 6 DOF 
        joint = PhysicsConstraints.createConstraint( parent.getPhysicsId(),  # get physics ID of the parent object
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
        wsFL=self.local_data['wheelFL'].getAngularVelocity(True)
        wsFR=self.local_data['wheelFR'].getAngularVelocity(True)
        wsRL=self.local_data['wheelRL'].getAngularVelocity(True)
        wsRR=self.local_data['wheelRR'].getAngularVelocity(True)
        return [wsFL[2], wsFR[2], wsRL[2], wsRR[2]]

    def getWheelAngle(self):
        """ Returns the accumulated wheel angle in radians"""
        # true parameters tell it velocities are local
        # wheels should be rotating about local Z axis
        wcFL=self.local_data['wheelFL'].localOrientation.to_euler()
        wcFR=self.local_data['wheelFR'].localOrientation.to_euler()
        wcRL=self.local_data['wheelRL'].localOrientation.to_euler()
        wcRR=self.local_data['wheelRR'].localOrientation.to_euler()
        return [wcFL[1], wcFR[1], wcRL[1], wcRR[1]]

    def AttachWheelToWheel(self,wheel1,wheel2):
        # add both wheels on each side to each other but with no
        # constraints on their motion so that no collision can be set
        # between them
        pass

    def GetWheels(self):
        # get pointers to and physicsIds of all objects
        # get wheel pointers - needed by wheel speed sensors and to
        # set up constraints
        # there should be 2 or 4 wheels - if only two wheels they should
        # be the front wheels
        scene = GameLogic.getCurrentScene()

        # front left wheel
        try:
            if self.blender_obj['WheelFLName']:
                self.local_data['wheelFL']=scene.objects[self.blender_obj['WheelFLName']]
        except:
            import traceback
            traceback.print_exc()       
              
        # check to see if the wheel has a parent, if so unparent it
        #if (self.local_data['wheelFL'].parent is not None):
        #    self.local_data['wheelFL'].removeParent()
 
        # front right wheel
        try:
            if self.blender_obj['WheelFRName']:
                self.local_data['wheelFR']=scene.objects[self.blender_obj['WheelFRName']]
        except:
            import traceback
            traceback.print_exc()          
 
        # see if back wheels exist - if not assume a two-wheeled vehicle
        # rear left wheel
        try:
            if self.blender_obj['WheelRLName']:
                self.local_data['wheelRL']=scene.objects[self.blender_obj['WheelRLName']]
        except:
            import traceback
            traceback.print_exc()   

        # rear right wheel
        try:
            if self.blender_obj['WheelRRName']:
                self.local_data['wheelRR']=scene.objects[self.blender_obj['WheelRRName']]
        except:
            import traceback
            traceback.print_exc() 
        
        # wheel ID's
        self.local_data['wheelFL_ID'] = self.local_data['wheelFL'].getPhysicsId()
        self.local_data['wheelFR_ID'] = self.local_data['wheelFR'].getPhysicsId()
        self.local_data['wheelRL_ID'] = self.local_data['wheelRL'].getPhysicsId()
        self.local_data['wheelRR_ID'] = self.local_data['wheelRR'].getPhysicsId()
 
