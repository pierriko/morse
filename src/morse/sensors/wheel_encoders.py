import logging; logger = logging.getLogger("morse." + __name__)
import math
import morse.core.sensor

class WheelEncodersClass(morse.core.sensor.MorseSensorClass):
    """ Odometer sensor """

    def __init__(self, obj, parent=None):
        """ Constructor method.
        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent. """
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        # Variables to store the accumulated rotation of the 4 wheels
        # wheel accumulated angle [rad]
        # self.local_data['rotFR'] = 0.0
        # self.local_data['rotFL'] = 0.0
        # self.local_data['rotRR'] = 0.0
        # self.local_data['rotRL'] = 0.0
        # # wheel angular speeds [rad/sec]
        # self.local_data['wFR'] = 0.0
        # self.local_data['wFL'] = 0.0
        # self.local_data['wRR'] = 0.0
        # self.local_data['wRL'] = 0.0

        # keep up with integer number of rotations to unwrap angles
        self._counts=[0,0,0,0]

        # keep up with previous angle for unwrapping
        self._prevRot=[0.0,0.0,0.0,0.0]
        logger.info('Component initialized')


    def default_action(self):
        """ Get the accumulated rotation of each wheel
        """
        # wheel #  -   wheel
        #    0     -    FR
        #    1     -    FL
        #    2     -    RR
        #    3     -    RL

        # get angular speed
        for index in self.robot_parent._wheel_index:
            if self.robot_parent._wheels[index] != None:
                new_index='ws_'+index
                self.local_data[new_index]=self.robot_parent._wheels[index].getAngularVelocity(True)

        # get wheel position            
        for index in self.robot_parent._wheel_index:
            if self.robot_parent._wheels[index] != None:
                new_index='rot_'+index
                self.local_data[new_index]=self.robot_parent._wheels[index].localOrientation.to_euler()
                new_index='orient_'+index
                self.local_data[new_index]=self.robot_parent._wheels[index].localOrientation
                new_index='pos_'+index
                self.local_data[new_index]=self.robot_parent._wheels[index].localPosition
        # wheelAngularSpeeds=self.robot_parent.getWheelSpeeds()
        # logger.debug("WHEELSPEED: (%.4f, %.4f, %.4f, %.4f)" % (wheelAngularSpeeds[0], wheelAngularSpeeds[1], wheelAngularSpeeds[2], wheelAngularSpeeds[3]))		
        # self.local_data['wFR'] = wheelAngularSpeeds[0]
        # self.local_data['wFL'] = wheelAngularSpeeds[1]
        # self.local_data['wRR'] = wheelAngularSpeeds[2]
        # self.local_data['wRL'] = wheelAngularSpeeds[3]

        # get angular distance traveled
        # wheelOrientations=self.robot_parent.getWheelAngle()   
        # logger.debug("WHEELANGLE: (%.4f, %.4f, %.4f, %.4f)" % (wheelOrientations[0], wheelOrientations[1], wheelOrientations[2], wheelOrientations[3]))				
        # # unwrap angles
        # #self.local_data['rotFR'] = self.unwrapAngle(wheelOrientations[0],0)+2*math.pi*self._counts[0]
        # #self.local_data['rotFL'] = self.unwrapAngle(wheelOrientations[1],1)+2*math.pi*self._counts[1]
        # #self.local_data['rotRR'] = self.unwrapAngle(wheelOrientations[2],2)+2*math.pi*self._counts[2]
        # #self.local_data['rotRL'] = self.unwrapAngle(wheelOrientations[3],3)+2*math.pi*self._counts[3]

        # self.local_data['rotFR'] = wheelOrientations[0]
        # self.local_data['rotFL'] = wheelOrientations[1]
        # self.local_data['rotRR'] = wheelOrientations[2]
        # self.local_data['rotRL'] = wheelOrientations[3]

        #print(self._counts)

    def unwrapAngle(self, curAngle, index):
        # get current angle between 0 and pi
        curAngle=curAngle%(2*math.pi)

        # go up by 2pi
        if (self._prevRot[index]>(300*math.pi/180+self._counts[index]*2*math.pi))and(curAngle<(60*math.pi/180)):
            self._counts[index]=self._counts[index]+1
            # go down by 2pi
        elif (self._prevRot[index]<(60*math.pi/180+self._counts[index]*2*math.pi))and(curAngle>(300*math.pi/180)):
            self._counts[index]=self._counts[index]-1

        # store previous value
        self._prevRot[index]=curAngle

        # return angle
        return curAngle
        
