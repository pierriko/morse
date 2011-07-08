import bpy
import math
import morse.builder.morsebuilder
from morse.builder.data import MORSE_MIDDLEWARE_DICT

class ComponentCreator(morse.builder.morsebuilder.AbstractComponent):
  def __init__(self, name, callingModule, blendname=None):
    """ ComponentCreator constructor

    name: (string) name of the Empty Blender object
    callingModule: (string) in ['calling.actuator_action', 'calling.sensor_action', 'calling.mw_action']
    blendname: (string) used for the middleware configuration (default: None)
      see morse.builder.data.MORSE_MIDDLEWARE_DICT
    """
    morse.builder.morsebuilder.AbstractComponent.__init__(self)
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.add() # default is Empty object
    self._blendobj = bpy.context.selected_objects[0]
    self._blendobj.name = name
    self._blendname = blendname # for middleware configuration
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.select_name(name = self._blendobj.name)
    bpy.ops.logic.sensor_add() # default is Always sensor
    sensor = self._blendobj.game.sensors.keys()[-1]
    self._blendobj.game.sensors[sensor].use_pulse_true_level = True
    bpy.ops.logic.controller_add(type='PYTHON')
    controller = self._blendobj.game.controllers.keys()[-1]
    self._blendobj.game.controllers[controller].mode = 'MODULE'
    self._blendobj.game.controllers[controller].module = callingModule
    self._blendobj.game.controllers[controller].link( sensor = 
        self._blendobj.game.sensors[sensor] )
    # no collision by default for components
    self._blendobj.game.physics_type = 'NO_COLLISION'

class SensorCreator(ComponentCreator):
  def __init__(self, name, classPath, className, blendname=None):
    ComponentCreator.__init__(self, name, 'calling.sensor_action', blendname)
    self.properties(Component_Tag = True, Class = className, 
        Path = classPath)

class ActuatorCreator(ComponentCreator):
  def __init__(self, name, classPath, className, blendname=None):
    ComponentCreator.__init__(self, name, 'calling.actuator_action', blendname)
    self.properties(Component_Tag = True, Class = className, 
        Path = classPath)

class MiddlewareCreator(ComponentCreator):
  def __init__(self, name, classPath, className, blendname=None):
    ComponentCreator.__init__(self, name, 'calling.mw_action', blendname)
    self.properties(Middleware_Tag = True, Class = className, 
        Path = classPath)
  def configure(self, component, config=None):
    """ Component bindings with middlewares (hooks)

    http://www.openrobots.org/morse/doc/latest/user/hooks.html#configuration
    """
    if not config:
      config = MORSE_MIDDLEWARE_DICT[self._blendname][component._blendname]
    morse.builder.morsebuilder.AbstractComponent._config.link(component, config)
    morse.builder.morsebuilder.AbstractComponent._config.write()

class Cube(morse.builder.morsebuilder.AbstractComponent):
  def __init__(self, name):
    morse.builder.morsebuilder.AbstractComponent.__init__(self)
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.mesh.primitive_cube_add()
    self._blendobj = bpy.context.selected_objects[0]
    self._blendobj.name = name
    # no collision by default for components
    self._blendobj.game.physics_type = 'NO_COLLISION'

class Cylinder(morse.builder.morsebuilder.AbstractComponent):
  def __init__(self, name):
    morse.builder.morsebuilder.AbstractComponent.__init__(self)
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.mesh.primitive_cylinder_add()
    self._blendobj = bpy.context.selected_objects[0]
    self._blendobj.name = name
    # no collision by default for components
    self._blendobj.game.physics_type = 'NO_COLLISION'

class Spot(morse.builder.morsebuilder.AbstractComponent):
  def __init__(self, name):
    morse.builder.morsebuilder.AbstractComponent.__init__(self)
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.lamp_add(type='SPOT')
    self._blendobj = bpy.context.selected_objects[0]
    self._blendobj.name = name
    self.rotate(y=-math.pi/2)
    spot = bpy.data.lamps[-1]
    spot.spot_size = math.pi/2
    spot.distance = 10
    # no collision by default for components
    self._blendobj.game.physics_type = 'NO_COLLISION'

class Camera(morse.builder.morsebuilder.AbstractComponent):
  def __init__(self, name):
    morse.builder.morsebuilder.AbstractComponent.__init__(self)
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.camera_add()
    self._blendobj = bpy.context.selected_objects[0]
    self._blendobj.name = name
    # looking in +x
    self.rotate(x=math.pi/2, z=-math.pi/2)
    # no collision by default for components
    self._blendobj.game.physics_type = 'NO_COLLISION'

def test():
  # add a MotionControler object
  motion = ActuatorCreator("Motion_Controller", 
      "morse/actuators/v_omega", "VWActuatorClass", "morse_vw_control")
  # add a ROS Middleware object
  ros = MiddlewareCreator("ROS_Empty", 
      "morse/middleware/ros_mw", "ROSClass", "ros_empty")
  # add a GPS sensor
  gps = SensorCreator("GPS", 
      "morse/sensors/gps", "GPSClass", "morse_GPS")
  # add an Odometry sensor
  odometry = SensorCreator("Odometry", 
      "morse/sensors/odometry", "OdometryClass", "morse_odometry")
  # add a Pose sensor
  pose = SensorCreator("Pose_sensor", 
      "morse/sensors/pose", "PoseClass", "morse_pose")
  mesh = Cylinder("PoseCylinder")
  mesh.scale = (.1,.1,.2)
  pose.append(mesh)
  # add a Proximity sensor
  proximity = SensorCreator("Proximity", 
      "morse/sensors/proximity", "ProximitySensorClass", "morse_proximity")
  proximity.properties(Range = 30.0)


"""
# test the (experimental) Morse Components Creator
import sys
sys.path.append("/usr/local/lib/python3.1/dist-packages")
import morse.builder.creator
morse.builder.creator.test()
"""

