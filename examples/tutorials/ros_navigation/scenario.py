from morse.builder import *

# Append NavPR2 robot to the scene
james = NavPR2()
james.add_interface('ros')
james.translate(x=2.5, y=3.2, z=0.0)

# Keyboard control
keyboard = Keyboard()
james.append(keyboard)

# Set scenario
env = Environment('tum_kitchen/tum_kitchen')
env.aim_camera([1.0470, 0, 0.7854])
