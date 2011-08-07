import GameLogic
import math
import morse.core.sensor

class WheelEncodersClass(morse.core.sensor.MorseSensorClass):
    """ Odometer sensor """

    def __init__(self, obj, parent=None):
        """ Constructor method.

        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent.
        """
        print ("######## ODOMETER '%s' INITIALIZING ########" % obj.name)
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        # Variables to store the accumulated rotation of the 4 wheels
		# wheel accumulated angle [rad]
        self.local_data['rotFR'] = 0.0
        self.local_data['rotFL'] = 0.0
        self.local_data['rotRR'] = 0.0
        self.local_data['rotRL'] = 0.0
		# wheel angular speeds [rad/sec]
        self.local_data['wFR'] = 0.0
        self.local_data['wFL'] = 0.0
        self.local_data['wRR'] = 0.0
        self.local_data['wRL'] = 0.0
        print ('######## ODOMETER INITIALIZED ########')


    def default_action(self):
        """ Get the accumulated rotation of each wheel
        """
        # wheel #  -   wheel
        #    0     -    FR
        #    1     -    FL
        #    2     -    RR
        #    3     -    RL
        
        # get angular speed
        wheelAngularSpeeds=self.robot_parent.getWheelSpeeds()
		logger.debug("WHEELSPEED: (%.4f, %.4f, %.4f, %.4f)" % (wheelAngularSpeeds[0], wheelAngularSpeeds[1], wheelAngularSpeeds[2], wheelAngularSpeeds[3]))		
        self.local_data['wFR'] = wheelAngularSpeeds[0]
        self.local_data['wFL'] = wheelAngularSpeeds[1]
        self.local_data['wRR'] = wheelAngularSpeeds[2]
        self.local_data['wRL'] = wheelAngularSpeeds[3]

        # get angular distance traveled
        wheelOrientations=self.robot_parent.getWheelAngle()   
		logger.debug("WHEELANGLE: (%.4f, %.4f, %.4f, %.4f)" % (wheelOrientations[0], wheelOrientations[1], wheelOrientations[2], wheelOrientations[3]))				
        self.local_data['rotFR'] = wheelOrientations[0]
        self.local_data['rotFL'] = wheelOrientations[1]
        self.local_data['rotRR'] = wheelOrientations[2]
        self.local_data['rotRL'] = wheelOrientations[3]

        
