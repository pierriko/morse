Linear and angular speed (V, W) actuator 
========================================

This actuator reads the values of linear and angular speed and applies
them to the robot as wheel speeds.  This controller is intended to be 
used with robots that derive from the MorsePhysicsRobotClass class and 
are differential drive (no steerable wheels).  

The actuator calculates the left and right angular wheel speeds necessary 
to produce the given velocity (v) and yaw rate(w) in the absence of wheel
slip.  If slip occurs  the actual robot velocity and yaw rate may be smaller 
than that commanded.

The angular wheel speeds are calculated by:
.. math::
	v_{ws,l}=\frac{v-\omega t_{w}}{2 R}
	v_{ws,r}=\frac{v+\omega t_{w}}{2 R}

where :math:`t_{w}` is the track width of the robot and R is the wheel radius.

Files 
-----

-  Blender: ``$MORSE_ROOT/data/morse/components/controllers/morse_vw_diff_drive_control.blend``
-  Python: ``$MORSE_ROOT/src/morse/actuators/v_omega_diff_drive.py``

Local data 
----------

-  **v**: (float) linear velocity
-  **w**: (float) angular velocity

Services
--------

- **set_speed**: (synchronous service) Modifies v and w according to its
  parameter
- **stop**: (synchronous service) Stop the robot (modifies v and w to 0.0)

Applicable modifiers 
--------------------

No available modifiers
