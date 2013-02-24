from morse.builder import *

robot = ATRV()

motion = MotionVW()
robot.append(motion)

camera = VideoCamera()
camera.translate(x=.25,z=.85)
camera.frequency(1)
camera.properties(
        capturing = False,
        cam_width = 128,
        cam_height = 128,
        cam_focal = 25.0,
        Vertical_Flip = True
    )
camera.profile()
robot.append(camera)

motion.add_stream('socket')
camera.add_stream('socket')

env = Environment('indoors-1/indoor-1')
env.aim_camera([1.0470, 0, 0.7854])
env.show_framerate()

