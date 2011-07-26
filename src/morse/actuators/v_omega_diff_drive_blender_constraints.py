import GameLogic
import morse.core.actuator

class VWDiffDriveActuatorClass(morse.core.actuator.MorseActuatorClass):
    """ Motion controller using linear and angular speeds

    This class will read linear and angular speeds (V, W)
    as input from an external middleware, and then apply them
    to the parent robot.  Differs from the standard V,W controller
    in that individual wheel speeds are controlled rather than 
    chassis speed
    """

    def __init__(self, obj, parent=None):
        print ('######## VW CONTROL INITIALIZATION ########')
        # Call the constructor of the parent class
        super(self.__class__,self).__init__(obj, parent)

        self.local_data['v'] = 0.0
        self.local_data['w'] = 0.0

        # get track width for calculating wheel speeds from yaw rate
        parent = self.robot_parent
        self.trackWidth = parent.local_data['trackWidth']
        self.radius = parent.local_data['wheelRadius']

        print ('######## CONTROL INITIALIZED ########')



    def default_action(self):
        """ Apply (v, w) to the parent robot. """

        # calculate desired wheel speeds and set them

        if (self.local_data['v']<0.005)and(self.local_data['w']<0.005):
            # below a certain desired speed, lock the wheels
            self.robot_parent.local_data['wheelFL'].setAngularVelocity([0.0,0.0,-0.00001],True)
            self.robot_parent.local_data['wheelFR'].setAngularVelocity([0.0,0.0,-0.00001],True)
            self.robot_parent.local_data['wheelRL'].setAngularVelocity([0.0,0.0,0.00001],True)
            self.robot_parent.local_data['wheelRR'].setAngularVelocity([0.0,0.0,0.00001,True)            
            #print('stopping')
            pass
        else:
            # left and right wheel speeds in m/s
            v_ws_l=(2*self.local_data['v']-self.local_data['w']*self.trackWidth)/2
            v_ws_r=(2*self.local_data['v']+self.local_data['w']*self.trackWidth)/2

            # convert to angular speeds
            w_ws_l=v_ws_l/self.radius
            w_ws_r=v_ws_r/self.radius
            # set wheel speeds - front and rear wheels have the same speed
            self.robot_parent.local_data['wheelFL'].setAngularVelocity([0.0,0.0,w_ws_l],True)
            self.robot_parent.local_data['wheelFR'].setAngularVelocity([0.0,0.0,w_ws_r],True)
            self.robot_parent.local_data['wheelRL'].setAngularVelocity([0.0,0.0,w_ws_l],True)
            self.robot_parent.local_data['wheelRR'].setAngularVelocity([0.0,0.0,w_ws_r],True)
        #print(w_ws_l,w_ws_r,self.local_data['v'],self.local_data['w'])



