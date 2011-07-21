Engine force and steer angle actuator 
========================================

This actuator reads the values of engine force, braking force, and steer angle and applies them to the robot's wheels using the Bullet physics API.  It currently assumes a four-wheeled, front wheel steerable vehicle with wheels 0 and 1 being the front wheels and wheels 2 and 3 being the rear.

Files 
-----

-  Blender: ``$MORSE_ROOT/data/morse/components/controllers/morse_steer_force_control.blend``
-  Python: ``$MORSE_ROOT/src/morse/actuators/steer_force.py``

Local data 
----------

-  **steer**: (float) steer angle in degrees (+ to the right, - to the left)
-  **force**: (float) engine force
-  **brake**: (float) braking force

Adjustable parameters
---------------------

- 4wd (boolean) - The 4wd boolean in the **Logic Editor >> Game Properties** panel determines if engine force is applied to all four wheels or only the two rear wheels.  Braking is applied to all four wheels regardless of this setting.


Applicable modifiers 
--------------------

No available modifiers
