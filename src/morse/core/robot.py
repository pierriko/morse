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

        # make sure wheels are not children of the robot
        needRestart=False
        if (bpy.data.objects[self.blender_obj['WheelFLName']].parent is not None):
            bpy.ops.object.select_name(name=self.blender_obj['WheelFLName'])
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #self.local_data['wheelFL'].removeParent()
            needRestart=True
        if (bpy.data.objects[self.blender_obj['WheelFRName']].parent is not None):    
            bpy.ops.object.select_name(name=self.blender_obj['WheelFRName'])
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #self.local_data['wheelFR'].removeParent()
            needRestart=True
        if (bpy.data.objects[self.blender_obj['WheelRLName']].parent is not None):
            bpy.ops.object.select_name(name=self.blender_obj['WheelRLName'])
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #self.local_data['wheelRL'].removeParent()
            needRestart=True
        if (bpy.data.objects[self.blender_obj['WheelRRName']].parent is not None):
            bpy.ops.object.select_name(name=self.blender_obj['WheelRRName'])
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            #self.local_data['wheelRR'].removeParent()
            needRestart=True

        # get wheel radius
        self.local_data['WheelRadius']=self.GetWheelRadius(self.blender_obj['WheelFLName'])

        # scene must be restarted for changes to parents to take effect - no clue why 
        #if (needRestart):
        #    scene.restart()


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
        self.local_data['vehicle'] = PhysicsConstraints.getVehicleConstraint(cid)
            
        # read the needed parameters from the blender object properties
        self.ReadGenericParameters()
        self.ReadParameters()
        # get references to all of the wheels
        self.GetWheels() 

        # get physics ID's of wheels
        self.local_data['wheelFL_ID'] = self.local_data['wheelFL'].getPhysicsId()
        self.local_data['wheelFR_ID'] = self.local_data['wheelFR'].getPhysicsId()
        self.local_data['wheelRL_ID'] = self.local_data['wheelRL'].getPhysicsId()
        self.local_data['wheelRR_ID'] = self.local_data['wheelRR'].getPhysicsId()
 
        
        # get track width
        self.local_data['trackWidth']=self.GetTrackWidth();
        
        # add wheels
        # front wheels - steerable if property is true
        self.AttachWheelToBody(self.local_data['wheelFL'], self.blender_obj, self._HasSteering)
        self.AttachWheelToBody(self.local_data['wheelFR'], self.blender_obj, self._HasSteering)
        # rear wheels - never steerable
        self.AttachWheelToBody(self.local_data['wheelRL'], self.blender_obj, False)
        self.AttachWheelToBody(self.local_data['wheelRR'], self.blender_obj, False)
            
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
        joint=self.local_data['vehicle'].addWheel(wheel,wheelPos,wheelAttachDirLocal,wheelAxleLocal,self._SuspensionRestLength,self.local_data['WheelRadius'],hasSteering)
 
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

    def GetWheelRadius(self, wheelName):
        dims=bpy.data.objects[wheelName].dimensions
        # average the y and z dimension to get diameter - divide by 2 for radius
        return (dims[1]+dims[2])/4

    def TireModel():
        ## setup aliases
        #vehicle = PC.getVehicleConstraint(G.car["cid"])
        #cont = G.getCurrentController()
        #keys = cont.sensors["key"].events
        #lst=G.getCurrentScene()
        #whfl=lst.objects['Wheel3']
        #whfr=lst.objects['Wheel2']
        #bare=lst.objects['bare']
        oribm = self.blender_obj.orientation
        orib = acos(oribm[2][2])
        # 180/pi = 57.29..... convert to degrees
        oriwfr=(acos(self.local_data['wheelFR'].localOrientation[1][1])*57.29577951)
        oriwfl=(acos(self.local_data['wheelFL'].localOrientation[1][1])*57.29577951)
        
        ## Model Parameters
        Par = [9.8, 1, 1.45, 1.56/2, 1.54/2, .4, 117.1, 3.5, 3.5, 3.0, 3.0, 162.7, .2035, .2035, .2035, .2035, .33, .33, .33, .33]
        
        g = Par[0] 
        Lf = Par[1] 
        Lr = Par[2] 
        Tf = Par[3] 
        Tr = Par[4] 
        hcg = Par[5] 
        Ms = Par[6] 
        Mufl = Par[7] 
        Mufr = Par[8] 
        Murl = Par[9] 
        Murr = Par[10] 
        Iz = Par[11] 
        Iwfl = Par[12] 
        Iwfr = Par[13] 
        Iwrl = Par[14] 
        Iwrr = Par[15] 
        Rwfl = Par[16] 
        Rwfr = Par[17] 
        Rwrl = Par[18] 
        Rwrr = Par[19] 

        # Inputs = [ Yaw Vx Vy r wfl wfr wrl wrr ax ay Fzfl Fzfr Fzrl Fzrr Deltafl Deltafr mufl mufr murl murr ]

        ##    Yaw = u[1] 
        Vx=self.blender_obj.getLinearVelocity(True)[0]
        Vy=self.blender_obj.getLinearVelocity(True)[1]
        #Vx = bare["speed"]*cos(bare.localOrientation[1][1]) 
        #Vy = bare["speed"]*sin(bare.localOrientation[1][1]) 
        r = self.blender_obj.getAngularVelocity()[2]
        wfl =  self.local_data['vehicle'].getWheelRotation(0) 
        wfr =  self.local_data['vehicle'].getWheelRotation(1) 
        wrl =  self.local_data['vehicle'].getWheelRotation(2) 
        wrr =  self.local_data['vehicle'].getWheelRotation(3) 
        ##        ax = u[9]  
        ##        ay = u[10] 
        Fzfl = Ms/4
        Fzfr = Ms/4 
        Fzrl = Ms/4 
        Fzrr = Ms/4
        Deltafl=bare["al"]*.017453292
        Deltafr=bare["ar"]*.017453292
        mufl = Mufl
        mufr = Mufr
        murl = Murl 
        murr = Murr


        Vx1 = Vx+0.5*Tf*r 
        Vx2 = Vx-0.5*Tf*r 
        Vx3 = Vx+0.5*Tr*r 
        Vx4 = Vx-0.5*Tr*r 

        Vy1 = Vy+Lf*r 
        Vy2 = Vy+Lf*r 
        Vy3 = Vy-Lr*r 
        Vy4 = Vy-Lr*r 

        z1 = Vx1+1j*Vy1 
        SlipAnglefl = (Deltafl-cmath.phase(z1))*sgn(abs(z1)) 
        Vxu1 = abs(z1)*cos(SlipAnglefl)
        Slipfl = slip(Vxu1,wfl,Rwfl) 

        z2 = Vx2+1j*Vy2 
        SlipAnglefr = (Deltafr-cmath.phase(z2))*sgn(abs(z2)) 
        Vxu2 = abs(z2)*cos(SlipAnglefr)
        Slipfr = slip(Vxu2,wfr,Rwfr) 

        z3 = Vx3+1j*Vy3
        SlipAnglerl = -cmath.phase(z3)*sgn(abs(z3)) 
        Vxu3 = abs(z3)*cos(SlipAnglerl)
        Sliprl = slip(Vx3,wrl,Rwrl) 
          
        z4 = Vx4+1j*Vy4 
        SlipAnglerr = -cmath.phase(z4)*sgn(abs(z4)) 
        Vxu4 = abs(z4)*cos(SlipAnglerr) 
        Sliprr = slip(Vx4,wrr,Rwrr)

    #=============================================================================
    #	Tire Forces
    #=============================================================================

        Fxfl = 0
        Fyfl = 0
        Mzfl = 0
        TRfl = 0 
        Fxfr = 0
        Fyfr = 0
        Mzfr = 0
        TRfr = 0 
        Fxrl = 0
        Fyrl = 0
        Mzrl = 0
        TRrl = 0 
        Fxrr = 0
        Fyrr = 0
        Mzrr = 0
        TRrr = 0 

        if Fzfl>0:
                [Fxfl, Fyfl, Mzfl] = Pacejka(Slipfl, SlipAnglefl, Fzfl, mufl) 
                TRfl = Rwfl*sgn(wfl)*(0.01+3.24*0.005*(3.6*abs(Vxu1)/160)**0.25)*Fzfl+sgn(wfl) 
                Fyfl = Fyfl*sgn( 50*abs(Vy)+abs(Deltafl) ) 


        if Fzfr>0:
                [Fxfr, Fyfr, Mzfr] = Pacejka(Slipfr, SlipAnglefr, Fzfr, mufr) 
                TRfr = Rwfr*sgn(wfr)*(0.01+3.24*0.005*(3.6*abs(Vxu2)/160)**0.25)*Fzfr+sgn(wfr) 
                Fyfr = Fyfr*sgn( 50*abs(Vy)+abs(Deltafr)) 


        if Fzrl>0:
                [Fxrl, Fyrl, Mzrl] = Pacejka(Sliprl, SlipAnglerl, Fzrl, murl) 
                TRrl = Rwrl*sgn(wrl)*(0.01+3.24*0.005*(3.6*abs(Vxu3)/160)**0.25)*Fzrl+sgn(wrl) 
                Fyrl = Fyrl*sgn(50*abs(Vy)) 


        if Fzrr>0:
                [Fxrr, Fyrr, Mzrr] = Pacejka(Sliprr, SlipAnglerr, Fzrr, murr) 
                TRrr = Rwrr*sgn(wrr)*(0.01+3.24*0.005*(3.6*abs(Vxu4)/160)**0.25)*Fzrr+sgn(wrr) 
                Fyrr = Fyrr*sgn(50*abs(Vy))
        sys = [ Fxfl, Fxfr, Fxrl, Fxrr, Fyfl, Fyfr, Fyrl, Fyrr, Mzfl, Mzfr, Mzrl, Mzrr, TRfl, TRfr, TRrl, TRrr, Slipfl, Slipfr, Sliprl, Sliprr, SlipAnglefl, SlipAnglefr, SlipAnglerl, SlipAnglerr]
        return sys

    #=============================================================================
    # Sign function
    #=============================================================================
    def sgn(x):
            if abs(x)>1 and x>0:
                return 1
            elif abs(x)>1 and x<0:
                return -1
            else:
                return x
    #=============================================================================
    # Slip Computation
    #=============================================================================
    def slip(Vx,w,Rw):
        if abs(Vx)>abs(Rw*w):
            Vxmax = abs(Vx) 
            Vxmin = abs(Rw*w) 
        else:
            Vxmax = abs(Rw*w)   
            Vxmin = abs(Vx)
        dVx = Rw*w-Vx 
        Vxmax = Vxmax+0.001*exp(-4*Vxmax) 
        slip = sgn(0.2*dVx)*(1-Vxmin/Vxmax)
        return slip

    #=============================================================================
    # Tire Model
    #=============================================================================
    def Pacejka(Lambda,Alpha,Fz,Mu):
        ''' calculate the lateral, longitudinal, and aligning torque '''
        # lamdba - longitudinal slip
        # Alpha - slip angle
        # Fz - normal force
        # Mu - friction coefficient
        #Alpha:absolute value
        A0 = 1.65000 
        A1 = -34.0 
        A2 = 1250.0 
        A3 = 3036.0 
        A4 = 12.80 
        A5 = 0.00501 
        A6 = -0.02103 
        A7 = 0.77394 
        A8 = 0.0022890 
        A9 = 0.013442 
        A10 = 0.003709 
        A11 = 19.1656 
        A12 = 1.21356 
        A13 = 6.26206 
        B0 = 2.37272 
        B1 = -9.46000 
        B2 = 1490.00 
        B3 = 130.000 
        B4 = 276.000 
        B5 = 0.08860 
        B6 = 0.00402 
        B7 = -0.06150 
        B8 = 1.20000 
        B9 = 0.02990 
        B10 = -0.17600 
        C0 = 2.34000 
        C1 = 1.4950 
        C2 = 6.416654 
        C3 = -3.57403 
        C4 = -0.087737 
        C5 = 0.098410 
        C6 = 0.0027699 
        C7 = -0.0001151 
        C8 = 0.1000 
        C9 = -1.33329 
        C10 = 0.025501 
        C11 = -0.02357 
        C12 = 0.03027 
        C13 = -0.0647 
        C14 = 0.0211329 
        C15 = 0.89469 
        C16 = -0.099443 
        C17 = -3.336941 
        Gamma = 0 
        Lambda = 100*Lambda 
        Alpha = Alpha*180/pi 
        Fz = Fz/1000 
        if Alpha > 90:
            Alpha = 180-Alpha 
        elif Alpha < -90:
            Alpha = -180-Alpha 


        # Longitudinal Force
        C = B0 
        Alpa = asin(sin(abs(Alpha*pi/180)))*180/pi 
        D = (B1*Fz**2+B2*Fz)*exp(-0.03*Alpa) 
        BCD = (B3*Fz**2+B4*Fz)*exp(-B5*Fz)*exp(-0.1*Alpa-1) 
        B = BCD/(C*D) 
        Sh = B9*Fz+B10 
        Sv = 0.0 
        X = Lambda+Sh 
        E = (B6*Fz**2+B7*Fz+B8)*exp(0.01*Alpa) 
        Fx = 0.8*(D*sin(C*atan(B*X-E*(B*X-atan(B*X)))))+Sv 

        # Lateral Force
        C = A0*exp(-0.01*abs(Lambda)) 
        D = (A1*Fz**2+A2*Fz)*exp(-0.01*abs(Lambda)) 
        BCD = A3*sin(atan(Fz/A4)*2.0)*(1.0-A5*abs(Gamma)) 
        B = BCD/(C*D) 
        Sh = A9*Fz+A10+A6*Gamma 
        Sv = A11*Fz*Gamma+A12*Fz+A13 
        X = Alpha+Sh 
        E = (A6*Fz+A7) 
        Fy = (D*sin(C*atan(B*X-E*(B*X-atan(B*X)))))+Sv 

        # Self-Aligning Torque
        C = C0 
        D = (C1*Fz**2+C2*Fz) 
        BCD = (C3*Fz**2+C4*Fz)*(1-(C6*abs(Gamma)))*exp(-C5*Fz) 
        B = BCD/(C*D) 
        Sh = C11*Gamma+C12*Fz+C13 
        Sv = (C14*Fz**2+C15*Fz)*Gamma+C16*Fz+C17 
        X = Alpha+Sh 
        E = (C7*Fz**2+C8*Fz+C9)*(1.0-C10*abs(Gamma)) 
        Mz = (D*sin(C*atan(B*X-E*(B*X-atan(B*X)))))+Sv 
        Mz = 0.001*Mz 


        Fx = Mu*Fx/0.85 
        Fy = Mu*Fy/0.85 
        Mz = Mu*Mz/0.85
        # return longitudinal force, lateral force, and self-aligning torque
        return[Fx,Fy,Mz]
    
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
        result = parent.getVectTo(wheel);
        # result is a unit vector (result[2]) and a length(result[0])
        # multiply them together to get the complete vector
        wheelPos=result[0]*result[2]
        logger.debug("Wheel Position: (%.4f, %.4f, %.4f)" % (wheelPos[0], wheelPos[1], wheelPos[2]))
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
    
