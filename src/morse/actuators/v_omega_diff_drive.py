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
            # lock the wheel when velocity is below a given threshold
            # get the current orientation and lock the wheels there
            #curOrient=self.robot_parent.getWheelCount()
            #self.robot_parent.local_data['wheelFLJoint'].setParam(3,0.0,0.0) # no rotation about Y axis
            #self.robot_parent.local_data['wheelFRJoint'].setParam(3,0.0,0.0) # no rotation about Y axis
            #self.robot_parent.local_data['wheelRLJoint'].setParam(3,0.0,0.0) # no rotation about Y axis
            #self.robot_parent.local_data['wheelRRJoint'].setParam(3,0.0,0.0) # no rotation about Y axis

            #self.robot_parent.local_data['wheelFLJoint'].setParam(3,curOrient[0],curOrient[0]) # no rotation about Y axis
            #self.robot_parent.local_data['wheelFRJoint'].setParam(3,curOrient[1],curOrient[1]) # no rotation about Y axis
            #self.robot_parent.local_data['wheelRLJoint'].setParam(3,curOrient[2],curOrient[2]) # no rotation about Y axis
            #self.robot_parent.local_data['wheelRRJoint'].setParam(3,curOrient[3],curOrient[3]) # no rotation about Y axis
              
            #self.robot_parent.local_data['wheelFL'].applyRotation([0.0,0.0,0.0],True)
            #self.robot_parent.local_data['wheelFR'].applyRotation([0.0,0.0,0.0],True)
            #self.robot_parent.local_data['wheelRL'].applyRotation([0.0,0.0,0.0],True)
            #self.robot_parent.local_data['wheelRR'].applyRotation([0.0,0.0,0.0],True)

            self.robot_parent.local_data['wheelFLJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelFRJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelRLJoint'].setParam(9,0,100.0)
            self.robot_parent.local_data['wheelRRJoint'].setParam(9,0,100.0)

            #print('stopping')
            pass
        else:
            # left and right wheel speeds in m/s
            v_ws_l=(2*self.local_data['v']-self.local_data['w']*self.trackWidth)/2
            v_ws_r=(2*self.local_data['v']+self.local_data['w']*self.trackWidth)/2

            # convert to angular speeds
            w_ws_l=v_ws_l/self.radius
            w_ws_r=v_ws_r/self.radius
            
            #unlock wheels in case we are just starting up
            #self.robot_parent.local_data['wheelFLJoint'].setParam(3,-10000.0,10000.0) # allow rotation about X axis
            #self.robot_parent.local_data['wheelFRJoint'].setParam(3,-10000.0,10000.0) # allow rotation about Y axis
            #self.robot_parent.local_data['wheelRLJoint'].setParam(3,-10000.0,10000.0) # allow rotation about Y axis
            #self.robot_parent.local_data['wheelRRJoint'].setParam(3,-10000.0,10000.0) # allow rotation about Y axis            
            
            # set wheel speeds - front and rear wheels have the same speed
            self.robot_parent.local_data['wheelFLJoint'].setParam(9,w_ws_l,100.0)
            self.robot_parent.local_data['wheelFRJoint'].setParam(9,w_ws_r,100.0)
            self.robot_parent.local_data['wheelRLJoint'].setParam(9,w_ws_l,100.0)
            self.robot_parent.local_data['wheelRRJoint'].setParam(9,w_ws_r,100.0)




