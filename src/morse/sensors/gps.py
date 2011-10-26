import logging; logger = logging.getLogger("morse." + __name__)
import GameLogic
import morse.core.sensor
from math import atan2, pow, sqrt   


class GPSClass(morse.core.sensor.MorseSensorClass):
    """ Class definition for the gyroscope sensor.
    Sub class of Morse_Object. """

    def __init__(self, obj, parent=None):
        """ Constructor method.
        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent. """
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        #logger.setLevel(logging.DEBUG)
        
        self.local_data['x'] = 0.0
        self.local_data['y'] = 0.0
        self.local_data['z'] = 0.0
        self.local_data['course'] = 0.0
        self.local_data['speed'] = 0.0
        self.local_data['vertSpeed'] = 0.0
        self.local_data['velX'] = 0.0
        self.local_data['velY'] = 0.0
        self.local_data['velZ'] = 0.0

        # Variables to store the previous position
        # needed to calculate the GPS velocity
        self.ppx = 0.0
        self.ppy = 0.0
        self.ppz = 0.0
 
        # Tick rate is the real measure of time in Blender.
        # By default it is set to 60, regardles of the FPS
        # If logic tick rate is 60, then: 1 second = 60 ticks
        # needed to scale change in position to get speed 
        self.ticks = GameLogic.getLogicTicRate()

        logger.info('Component initialized')


    def default_action(self):
        """ Main function of this component. """
        x = self.position_3d.x
        y = self.position_3d.y
        z = self.position_3d.z
        logger.debug("POSITION: (%.4f, %.4f, %.4f)" % (x,y,z))

        # Store the data acquired by this sensor that could be sent
        #  via a middleware.
        self.local_data['x'] = float(x)
        self.local_data['y'] = float(y)
        self.local_data['z'] = float(z)

        # Compute the difference in positions with the previous loop
        dx = self.position_3d.x - self.ppx
        dy = self.position_3d.y - self.ppy
        dz = self.position_3d.z - self.ppz

        # Scale the speeds to the time used by Blender
        # and store the velocity vector in world coordinates
        self.local_data['velX']=dx * self.ticks
        self.local_data['velY']=dy * self.ticks
        self.local_data['velZ']=dz * self.ticks

        # also post the data as course and speed over ground and vertical
        # speed some most receivers provide this rather than (x,y,z) velocity
        # calculate the direction of the velocity vector
        self.local_data['course']=atan2(self.local_data['velY'],self.local_data['velX'])
        # calculate the magnitude of the velocity vector
        self.local_data['speed']=sqrt(pow(self.local_data['velX'],2)+pow(self.local_data['velY'],2))
        # vertical velocity component
        self.local_data['vertSpeed']=self.local_data['velZ']

        #BELOW IS EXPERIMENTAL AND FOR COMPARISON ONLY!!!!!!!!!        
        # get the global linear velocity of the gps
        vels=self.blender_obj.getLinearVelocity(False)
        logger.debug("GLOBAL SPEED: (%.4f, %.4f, %.4f)" % (vels[0], vels[1], vels[2]))
        # get the global linear velocity of the gps
        vels=self.blender_obj.getLinearVelocity(True)
        logger.debug("LOCAL SPEED: (%.4f, %.4f, %.4f)" % (vels[0], vels[1], vels[2]))

        
