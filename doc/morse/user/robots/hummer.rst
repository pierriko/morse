Hummer car robot
================

This is a generic car like robot. It is driven using steering, power and braking as provided by the :doc:`steer/force actuator <../actuators/steer_force>`.
This vehicle uses the Blender `vehicle wrapper <http://www.blender.org/documentation/blender_python_api_2_59_0/bge.types.html#bge.types.KX_VehicleWrapper>`_ constraint, to give it a realistic behaviour, including the interaction of the wheels with the ground and suspension.

Files
-----

- Blender: ``$MORSE_ROOT/data/morse/robots/hummer.blend``
- Python: ``$MORSE_ROOT/src/morse/robots/hummer.py``

Adjustable parameters
---------------------

Use the **Properties >> Physics** panel in Blender to adjust the **Mass** of the robot.

The friction coefficient of the robot can be adjusted in its .blend file. When the robot
is selected, the **Logic Editor** panel will display its **Game Properties**.

- **Friction**: (float) Wheel's friction to the ground. Determines how fast the robot can accelerate from a standstill.
    Also affects steering wheel's ability to turn the vehicle.
    A value of ``0`` gives very low acceleration. Higher values permit a higher acceleration.
- **Stiffness** (float) Affects how quickly the suspension will 'spring back': 0 = No Spring back; 
    0.001 and higher = faster spring back
- **Influence**:  (float) rolling Influence: How easy it will be for the vehicle 
    to roll over while turning: 0 = Little to no rolling over; 0.1 and higher = 
    easier to roll over. Wheels that loose contact with the ground will be unable 
    to steer the vehicle as well.
- **Damping**:  (float) - Determines how much the suspension will absorb the 
    compression: 0 = Bounce like a super ball; greater than 0 = less bounce
- **Compression**:  (float) Resistance to compression of the overall suspension 
    length: 0 = Compress the entire length of the suspension; Greater than 0 = 
    compress less than the entire suspension length; 10 = almost no compression
- **4wd**:  (boolean) - If true, all four wheels are driven.  If false only the 
    back two wheels are driven.
- **Suspension_rest_length**:  (float) - the length of the suspension when it's 
    fully extended
- **Wheel_radius**:  (float) - radius of the physics (not visible model) wheel. 
    Turn on Game:Show Physics Visualization to see a purple line representing 
    the wheel radius.
