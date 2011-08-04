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

        self.local_data['x'] = 0.0
        self.local_data['y'] = 0.0
        self.local_data['z'] = 0.0
        self.local_data['course'] = 0.0
        self.local_data['speed'] = 0.0
        self.local_data['vertSpeed'] = 0.0
        self.local_data['velX'] = 0.0
        self.local_data['velY'] = 0.0
        self.local_data['velZ'] = 0.0

        logger.info('Component initialized')


    def default_action(self):
        """ Main function of this component. """
        x = self.position_3d.x
        y = self.position_3d.y
        z = self.position_3d.z

        # Store the data acquired by this sensor that could be sent
        #  via a middleware.
        self.local_data['x'] = float(x)
        self.local_data['y'] = float(y)
        self.local_data['z'] = float(z)
        
        # get the global linear velocity of the gps
        vels=self.blender_obj.getLinearVelocity(False)
        # calculate the direction of the velocity vector
        self.local_data['course']=atan2(vels[1],vels[0])
        # calculate the magnitude of the velocity vector
        self.local_data['speed']=sqrt(pow(vels[0],2)+pow(vels[1],2))
        # vertical velocity component
        self.local_data['vertSpeed']=vels[2]
        
        self.local_data['velX']=vels[0]
        self.local_data['velY']=vels[1]
        self.local_data['velZ']=vels[2]
        

