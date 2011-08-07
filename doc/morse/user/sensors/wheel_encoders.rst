GPS sensor
==========

This sensor emulates a set of wheel encoders providing the angular wheel speed and angular displacement of the vehicle's wheels.  This sensor can currently only be used with robots that derive from the MorsePhysicsRobot class.

Files
-----
- Blender: ``$MORSE_ROOT/data/morse/components/sensors/morse_wheel_encoders.blend``
- Python: ``$MORSE_ROOT/src/morse/sensors/wheel_encoders.py``

Local data
~~~~~~~~~~
- **rotFL**: (float) accumulated angular displacement of the front left wheel [rad]
- **rotFR**: (float) accumulated angular displacement of the front right wheel [rad]
- **rotRL**: (float) accumulated angular displacement of the rear left wheel [rad]
- **rotRR**: (float) accumulated angular displacement of the rear right wheel [rad]

- **wFL**: (float) angular velocity of the front left wheel [rad/s]
- **wFR**: (float) angular velocity of the front right wheel [rad/s]
- **wRL**: (float) angular velocity of the rear left wheel [rad/s]
- **wRR**: (float) angular velocity of the rear right wheel [rad/s]

.. note:: Rotations are measured about the y-axis of the wheel objects.

Applicable modifiers
--------------------

None