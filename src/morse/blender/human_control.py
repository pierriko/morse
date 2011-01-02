
######################################################
#
#    human_control.py        Blender 2.55
#
#    Modified version of
#      view_camera.py by Gilberto Echeverria
#
#    Gilberto Echeverria
#    26 / 12 / 2010
#
######################################################

import Rasterizer
import GameLogic
import GameKeys
import math
import sys
if sys.version_info<(3,0,0):
    import Mathutils as mathutils
else:
    import mathutils

def move(contr):
    """ Read the keys for specific combinations
        that will make the camera move in 3D space. """
    # get the object this script is attached to
    human = contr.owner

    # set the movement speed
    speed = human['Speed']

    # Get sensor named Mouse
    keyboard = contr.sensors['All_Keys']

    # Default movement speed
    move_speed = [0.0, 0.0, 0.0]
    rotation_speed = [0.0, 0.0, 0.0]

    keylist = keyboard.events
    for key in keylist:
        # key[0] == GameKeys.keycode, key[1] = status
        if key[1] == GameLogic.KX_INPUT_ACTIVE:
            # Also add the key corresponding key for an AZERTY keyboard
            if key[0] == GameKeys.WKEY or key[0] == GameKeys.ZKEY:
                move_speed[0] = speed
            elif key[0] == GameKeys.SKEY:
                move_speed[0] = -speed
            # Also add the key corresponding key for an AZERTY keyboard
            elif key[0] == GameKeys.AKEY or key[0] == GameKeys.QKEY:
                rotation_speed[2] = speed
            elif key[0] == GameKeys.DKEY:
                rotation_speed[2] = -speed
            elif key[0] == GameKeys.RKEY:
                move_speed[1] = speed
            elif key[0] == GameKeys.FKEY:
                move_speed[1] = -speed

            # The second parameter of 'applyMovement' determines
            #  a movement with respect to the object's local
            #  coordinate system
            human.applyMovement( move_speed, True )
            human.applyRotation( rotation_speed, True )

            """
            if key[0] == GameKeys.UPARROWKEY:
                move_speed[0] = speed
            elif key[0] == GameKeys.DOWNARROWKEY:
                move_speed[0] = -speed
            elif key[0] == GameKeys.LEFTARROWKEY:
                rotation_speed[2] = speed
            elif key[0] == GameKeys.RIGHTARROWKEY:
                rotation_speed[2] = -speed
            elif key[0] == GameKeys.AKEY:
                move_speed[2] = speed
            elif key[0] == GameKeys.EKEY:
                move_speed[2] = -speed
            """

        elif key[1] == GameLogic.KX_INPUT_JUST_ACTIVATED:
            # Other actions activated with the keyboard
            # Reset camera to center
            if key[0] == GameKeys.NKEY and keyboard.positive:
                reset_view(contr)
            # Switch between look and manipulate
            elif key[0] == GameKeys.XKEY:
                toggle_manipulate(contr)


def human_actions(contr):
    """ Toggle the animation actions of the armature """
    # Get sensor named Mouse
    armature = contr.owner
    keyboard = contr.sensors['All_Keys']

    keylist = keyboard.events
    for key in keylist:
        # key[0] == GameKeys.keycode, key[1] = status
        if key[1] == GameLogic.KX_INPUT_JUST_ACTIVATED:
            # Keys for moving forward or turning
            if key[0] == GameKeys.WKEY or key[0] == GameKeys.ZKEY:
                armature['movingForward'] = True
            elif key[0] == GameKeys.SKEY:
                armature['movingBackward'] = True

            # TEST: Read the rotation of the bones in the armature
            elif key[0] == GameKeys.BKEY:
                read_pose(contr)
            elif key[0] == GameKeys.VKEY:
                reset_pose(contr)
        elif key[1] == GameLogic.KX_INPUT_JUST_RELEASED:
            if key[0] == GameKeys.WKEY or key[0] == GameKeys.ZKEY:
                armature['movingForward'] = False
            elif key[0] == GameKeys.SKEY:
                armature['movingBackward'] = False


def head_control(contr):
    """ Move the target of the head and camera

    Use the movement of the mouse to determine the rotation
    for the human head and camera. """
    # get the object this script is attached to
    human = contr.owner
    scene = GameLogic.getCurrentScene()
    target = scene.objects['Target_Empty']

    # If the manipulation mode is active, do nothing
    if human['Manipulate']:
        return

    # Get sensor named Mouse
    mouse = contr.sensors['Mouse']

    if mouse.positive:
        # get width and height of game window
        width = Rasterizer.getWindowWidth()
        height = Rasterizer.getWindowHeight()

        # get mouse movement from function
        move = mouse_move(human, mouse, width, height)

        # set mouse sensitivity
        sensitivity = human['Sensitivity']

        # Amount, direction and sensitivity
        left_right = move[0] * sensitivity
        up_down = move[1] * sensitivity

        target.applyMovement([0.0, left_right, 0.0], True)
        target.applyMovement([0.0, 0.0, up_down], True)

        # Reset mouse position to the centre of the screen
        # Using the '//' operator (floor division) to produce an integer result
        Rasterizer.setMousePosition(width//2, height//2)


def hand_control(contr):
    """ Move the hand following the mouse

    Use the movement of the mouse to determine the rotation
    for the IK arm (right arm) """
    # get the object this script is attached to
    human = contr.owner
    scene = GameLogic.getCurrentScene()
    target = scene.objects['IK_Target_Empty.R']

    # If the manipulation mode is inactive, do nothing
    if not human['Manipulate']:
        return
 
    # Get sensor named Mouse
    mouse = contr.sensors['Mouse']

    if mouse.positive:
        # get width and height of game window
        width = Rasterizer.getWindowWidth()
        height = Rasterizer.getWindowHeight()

        # get mouse movement from function
        move = mouse_move(human, mouse, width, height)

        # set mouse sensitivity
        sensitivity = human['Sensitivity']

        # Amount, direction and sensitivity
        left_right = move[0] * sensitivity
        up_down = move[1] * sensitivity

        target.applyMovement([0.0, left_right, 0.0], True)
        target.applyMovement([0.0, 0.0, up_down], True)

        # Reset mouse position to the centre of the screen
        # Using the '//' operator (floor division) to produce an integer result
        Rasterizer.setMousePosition(width//2, height//2)

    # Get sensors for mouse wheel
    wheel_up = contr.sensors['Wheel_Up']
    wheel_down = contr.sensors['Wheel_Down']

    if wheel_up.positive:
        front = 50.0 * sensitivity
        target.applyMovement([front, 0.0, 0.0], True)

    if wheel_down.positive:
        back = -50.0 * sensitivity
        target.applyMovement([back, 0.0, 0.0], True)


def read_pose(contr):
    armature = contr.owner
    print ("The armature is: '%s' (%s)" % (armature, type(armature)))

    for channel in armature.channels:
        if 'X_' not in channel.name:
            rotation = channel.joint_rotation
            print ("\tChannel '%s': (%.4f, %.4f, %.4f)" % (channel, rotation[0], rotation[1], rotation[2]))


def reset_pose(contr):
    armature = contr.owner
    for channel in armature.channels:     
        channel.rotation_mode = 6
        
        channel.joint_rotation = [0.0, 0.0, 0.0]

        rotation = channel.joint_rotation
        print ("\tChannel '%s': (%.4f, %.4f, %.4f)" % (channel, rotation[0], rotation[1], rotation[2]))

    armature.update()

def reset_view(contr):
    """ Make the human model look forward """
    human = contr.owner
    scene = GameLogic.getCurrentScene()
    target = scene.objects['Target_Empty']
    # Reset the Empty object to its original position
    target.localPosition = [1.3, 0.0, 1.7]


def toggle_manipulate(contr):
    """ Switch mouse control between look and manipulate """
    human = contr.owner
    scene = GameLogic.getCurrentScene()
    hand_target = scene.objects['IK_Target_Empty.R']
    head_target = scene.objects['Target_Empty']

    if human['Manipulate']:
        #Rasterizer.showMouse(False)
        human['Manipulate'] = False
        # Place the hand beside the body
        hand_target.localPosition = [0.0, -0.3, 0.5]
        head_target.setParent(human)
        head_target.localPosition = [1.3, 0.0, 1.7]
    else:
        #Rasterizer.showMouse(True)
        human['Manipulate'] = True
        head_target.setParent(hand_target)
        # Place the hand in a nice position
        hand_target.localPosition = [0.5, 0.0, 1.0]
        # Place the head in the same place
        head_target.localPosition = [0.0, 0.0, 0.0]


def toggle_sit(contr):
    """ Change the stance of the human model

    Make the human sit down or stand up, using a preset animation.
    """
    human = contr.owner

    # get the keyboard sensor
    sit_down_key = contr.sensors["sit_down"]

    # get the actuators
    sitdown = contr.actuators["sitdown"]
    standup = contr.actuators["standup"]

    # Sitdown
    if sit_down_key.positive and human['statusStandUp']:
        contr.activate(sitdown)
        human['statusStandUp'] = False

    # Standup
    elif sit_down_key.positive and not human['statusStandUp']:
        contr.activate(standup)
        human['statusStandUp'] = True


def mouse_move(human, mouse, width, height):
    """ Get the movement of the mouse as an X, Y coordinate. """
    # distance moved from screen center
    # Using the '//' operator (floor division) to produce an integer result
    x = width//2 - mouse.position[0]
    y = height//2 - mouse.position[1]

    # intialize mouse so it doesn't jerk first time
    try:
        human['mouseInit']
    except KeyError:
        x = 0
        y = 0
        # bug in Add Property
        # can't use True.  Have to use 1
        human['mouseInit'] = 1

    # return mouse movement
    return (x, y)
