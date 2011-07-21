Hummer Ackermann Steered Platform
=================================

A Hummer vehicle model modified from the Blender vehicle simulation tutorial at: `Blender 3d Club <http://www.blender3dclub.com/index.php?name=News&file=article&sid=93&theme=Printer>`_.  

This vehicle is set up differently than most others available in the Morse package. While it's movement can be controlled directly as with the other robots by setting its linear and angular velocities, it can also be controlled at a lower level by using the Bullet physics environment to set the engine force, braking force, and steering angle.  The steer_force actuator allows these properties to be controlled. 

Files
-----

- Blender: ``$MORSE_ROOT/data/morse/components/robots/hummer.blend``
- Python: ``$MORSE_ROOT/src/morse/robots/hummer.py``

Adjustable parameters
---------------------

Use the **Properties >> Physics** panel in Blender to adjust the **Mass** of the robot.

The friction coefficient of the robot can be adjusted in the **Properties >> Material** panel.

Several additional parameters can be set in the **Logic Editor >> Game Properties** panel.

Friction (float) sets the friction between the wheels and the ground.  This is different than the friction property discussed above which controls the friction of the vehicle's surface.  It affects how fast you can accelerate or brake and how well the front wheels can steer the vehicle.  0 = Very Slow Acceleration; 0.1 and higher = Faster Acceleration (more friction)

Stiffness (float) Affects how quickly the suspension will 'spring back': 0 = No Spring back; 0.001 and higher = faster spring back

Influence (float) rolling Influence: How easy it will be for the vehicle to roll over while turning: 0 = Little to no rolling over; 0.1 and higher = easier to roll over. Wheels that loose contact with the ground will be unable to steer the vehicle as well.

Damping (float) - Determines how much the suspension will absorb the compression: 0 = Bounce like a super ball; greater than 0 = less bounce

Compression (float) Resistance to compression of the overall suspension length: 0 = Compress the entire length of the suspension; Greater than 0 = compress less than the entire suspension length; 10 = almost no compression

4wd (boolean) - If true, all four wheels are driven.  If false only the back two wheels are driven.

Suspension_rest_length (float) - the length of the suspension when it's fully extended

Wheel_radius (float) - radius of the physics (not visible model) wheel.  Turn on Game:Show Physics Visualization to see a purple line representing the wheel radius.
