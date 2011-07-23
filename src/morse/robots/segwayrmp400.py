import GameLogic
import morse.core.robot


class SegwayRMP400Class(morse.core.robot.MorseRobotClass):
    """ Class definition for the Segway RMP400 base.
        Sub class of Morse_Object. """

		#
        #  This section runs only once to create the vehicle:
        #
        
        cont = GameLogic.getCurrentController()

        obj['init'] = 1
        physicsid = obj.getPhysicsId()
        vehicle = PhysicsConstraints.createConstraint(physicsid,0,11)
        obj['cid'] = vehicle.getConstraintId()
        self.vehicle = PhysicsConstraints.getVehicleConstraint(obj['cid'])
       
        # Wheel location from vehicle center
        wx = 1.3
        wy = 1.6
        wz = -.5

        #wheelAttachPosLocal:
        #Where the wheel is attach to the car based
        #on the vehicle's Center
        wheelAttachPosLocal = [wx, wy, wz]

        #wheelAttachDirLocal:
        #Direction the suspension is pointing
        wheelAttachDirLocal = [0,0,-1]

        #wheelAxleLocal:
        #Determines the rotational angle where the
        #wheel is mounted.
        wheelAxleLocal = [-1,0,0]

        #suspensionRestLength:
        #The length of the suspension when it's fully
        #extended:
        
        print('getting suspension length')
        #print(dir(self.blender_obj))
        #print(self.blender_obj['suspensionRestLength'])
        
        #suspensionRestLength = obj['suspensionRestLength']
        suspensionRestLength = .3

        #wheelRadius:
        #Radius of the Physics Wheel.
        #Turn on Game:Show Physics Visualization to see
        #a purple line representing the wheel radius.
        wheelRadius = .5	
        #wheelRadius = obj['wheelRadius']		

        #hasSteering:
        #Determines whether or not the coming wheel
        #assignment will be affected by the steering 
        #value:	
        hasSteering = 0

        #
        #	Front wheels:
        #

        scene = GameLogic.getCurrentScene()
        wheel1=scene.objects["rmp_wheel_atv.001"]

        #creates the first wheel using all of the variables 
        #created above:
        self.vehicle.addWheel(wheel1,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionRestLength,wheelRadius,hasSteering)
        
        #locates the second wheel:
        wheel2=scene.objects["rmp_wheel_atv.002"]

        #Positions this wheel on the opposite side of the car by using a
        #negative values for the x position.
        wheelAttachPosLocal = [-wx, wy, wz]

        #creates the second wheel:
        self.vehicle.addWheel(wheel2,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionRestLength,wheelRadius,hasSteering)

        #
        #	Rear Wheels:
        #

        #Change the hasSteering value to 0 so the rear wheels don't turn
        #when the steering value is changed.
        hasSteering = 0

        # Adjust the location the rear wheels are attached.  
        wx = 1.3
        wy = 2.3

        # Set the wheelAttachPosLocal to the new location for rear wheels:
        # -y moves the position toward the back of the car
        wheelAttachPosLocal = [wx ,-wy, wz]

        # locate the 3rd wheel:
        wheel3=scene.objects["rmp_wheel_atv.003"]

        #Creates the 3rd wheel (first rear wheel)
        self.vehicle.addWheel(wheel3,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionRestLength,wheelRadius,hasSteering)

        #Adjust the attach position for the next wheel:
        # changed to -x to place the wheel on the opposite side of the car
        # the same distance away from the vehicle's center
        wheelAttachPosLocal = [-wx ,-wy, wz]

        #locate the fourth wheel:
        wheel4=scene.objects["rmp_wheel_atv.004"]

        #create the last wheel using the above variables:
        self.vehicle.addWheel(wheel4,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionRestLength,wheelRadius,hasSteering)


        #The Rolling Influence:
        #How easy it will be for the vehicle to roll over while turning:
        #0 = Little to no rolling over
        # .1 and higher easier to roll over
        #Wheels that loose contact with the ground will be unable to
        #steer the vehicle as well.
        influence = 0.05
        #influence = obj['influence']
        self.vehicle.setRollInfluence(influence,0)
        self.vehicle.setRollInfluence(influence,1)
        self.vehicle.setRollInfluence(influence,2)
        self.vehicle.setRollInfluence(influence,3)

        #Stiffness:
        #Affects how quickly the suspension will 'spring back'
        #0 = No Spring back
        # .001 and higher = faster spring back
        stiffness = 15.0
        #stiffness = obj['stiffness']
        self.vehicle.setSuspensionStiffness(stiffness,0)
        self.vehicle.setSuspensionStiffness(stiffness,1)
        self.vehicle.setSuspensionStiffness(stiffness,2)
        self.vehicle.setSuspensionStiffness(stiffness,3)
        
        #Dampening:
        #Determines how much the suspension will absorb the
        #compression.
        #0 = Bounce like a super ball
        #greater than 0 = less bounce
        #damping = obj['damping']
        damping=10;
        self.vehicle.setSuspensionDamping(damping,0)
        self.vehicle.setSuspensionDamping(damping,1)
        self.vehicle.setSuspensionDamping(damping,2)
        self.vehicle.setSuspensionDamping(damping,3)
        
        #Compression:
        #Resistance to compression of the overall suspension length.
        #0 = Compress the entire length of the suspension
        #Greater than 0 = compress less than the entire suspension length.
        #10 = almost no compression
        #compression = obj['compression']
        compression = 2.0;
        self.vehicle.setSuspensionCompression(compression,0)
        self.vehicle.setSuspensionCompression(compression,1)
        self.vehicle.setSuspensionCompression(compression,2)
        self.vehicle.setSuspensionCompression(compression,3)

        #Friction:
        #Wheel's friction to the ground
        #How fast you can accelerate from a standstill.
        #Also affects steering wheel's ability to turn vehicle.
        #0 = Very Slow Acceleration:
        # .1 and higher = Faster Acceleration / more friction:
        #friction = obj['friction']
        friction=200.0;
        self.vehicle.setTyreFriction(friction,0)
        self.vehicle.setTyreFriction(friction,1)
        self.vehicle.setTyreFriction(friction,2)
        self.vehicle.setTyreFriction(friction,3)
              

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
