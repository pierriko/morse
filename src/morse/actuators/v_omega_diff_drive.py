import GameLogic
import morse.core.actuator
import math

class VWDiffDriveActuatorClass(morse.core.actuator.MorseActuatorClass):
    """ Motion controller using linear and angular speeds

    This class will read linear and angular speeds (V, W)
    as input from an external middleware, and then apply them
    to the parent robot.  Differs from the standard V,W controller
    in that individual wheel speeds are controlled rather than 
    chassis speed
    """

    def __init__(self, obj, parent=None):
        print ('######## VW Diff Drive CONTROL INITIALIZATION ########')
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        self.local_data['v'] = 0.0
        self.local_data['w'] = 0.0

        self._stopped=True

        # get track width for calculating wheel speeds from yaw rate
        parent = self.robot_parent
        self.trackWidth = parent.local_data['trackWidth']
        self.radius = parent.local_data['WheelRadius']

        print ('######## CONTROL INITIALIZED ########')

    def default_action(self):
        """ Apply (v, w) to the parent robot. """

        # calculate desired wheel speeds and set them
        #print('default action')
        
        if (abs(self.local_data['v'])<0.01)and(abs(self.local_data['w'])<0.01):
            # stop the wheel when velocity is below a given threshold
            self.robot_parent.local_data['wheelFLJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelFRJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelRLJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelRRJoint'].setParam(9,0,100.0)
            
            self._stopped=True
            #print('stopping')
            pass
        else:
            # this is need to "wake up" the physic objects if they have gone to sleep
            if (self._stopped==True):
                self.robot_parent.blender_obj.applyImpulse(self.robot_parent.blender_obj.position,(0.0,0.1,-0.000001))
            
            self._stopped=False
            
            # left and right wheel speeds in m/s
            v_ws_l=(2*self.local_data['v']-self.local_data['w']*self.trackWidth)/2
            v_ws_r=(2*self.local_data['v']+self.local_data['w']*self.trackWidth)/2

            # convert to angular speeds
            w_ws_l=v_ws_l/self.radius
            w_ws_r=v_ws_r/self.radius
            
            # set wheel speeds - front and rear wheels have the same speed
            self.robot_parent.local_data['wheelFLJoint'].setParam(9,w_ws_l,100.0)
            self.robot_parent.local_data['wheelFRJoint'].setParam(9,w_ws_r,100.0)
            self.robot_parent.local_data['wheelRLJoint'].setParam(9,w_ws_l,100.0)
            self.robot_parent.local_data['wheelRRJoint'].setParam(9,w_ws_r,100.0)




