Building a robot using physics constraints
==========================

This tutorial provides instructions on how to create a robot using basic physics constraints.  This 


bullet vehicle model does not use SAE standard - show picture
vehicle coordinate systems shouldn't matter - just mount the sensor the right way

same wheel mesh can't be used for both bullet and physics vehicle if cylinder collision box is used
cylinder box is turned so that z is out the top of the cylinder - bullet requires x out the side of the wheel
use convex hull, but impacts performance

changes in model between vehicle types:
---------------------------------------------------------------
wheels set to no collision for vehicle and rigid body for physics vehicle
body set to no sleeping for vehicle and no sleeping is off for physics vehicle
change actuator

Bullet Vehicle Constraint Robot
-----------------------

Coordinate System:
from rotated Hummer:
Vehicle body: y - out front of vehicle
                     x - out passenger's side of vehicle
                     z - up
                     
settings for this body frame
	
	#wheelAttachDirLocal:
	#Direction the suspension is pointing
	wheelAttachDirLocal = [0,0,-1]
    suspension points down toward the ground (-z)
	
	#wheelAxleLocal:
	#Determines the rotational angle where the
	#wheel is mounted.
	wheelAxleLocal = [0,1,0]
    wheels rotate about the vehicle's y-axis
    both of these settings are in the vehicle's frame
                     
Wheels:         x - out side of wheel
                     y - out back of wheel or front?
                     z - up
                     only local wheel frames matter - must apply rotation
     

this setup works, but the wheels do not appear to rotate properly

from documentation
http://www.tutorialsforblender3d.com/Game_Engine/Vehicle/Vehicle_1.html
vehicle body - movement is along y
y-axis is length.  
x-axis is width.  
z-axis is height

Tire model:  
y-axis is length.  
x-axis is width.  
z-axis is height
Note:  The vehicle wrapper uses the y-axis for movement. 

in original hummer model
body - y out front
        x out driver's side
        z up
wheels - x out drivers side of wheel
            y backward
            z up
	wheelAttachDirLocal = [0,0,-1]
	
	#wheelAxleLocal:
	#Determines the rotational angle where the
	#wheel is mounted.
	wheelAxleLocal = [-1,0,0]



Bullet Basic Physics Constraints Robot
-----------------------

Coordinate System:

wheels: x out side of wheel - rotates about x
            y and z shouldn't matter
            
body:  y out front
          x out passenger's side
          z up


problem with coordinate system is that the cylinder bounding box cannot be used for wheels because it assumes the cylinder rotates about z and bullet requires the wheels to rotate about x
solution is to replace the physics mesh with a cylinder and set a convex hull to it

on the object set up an always sensor, an and controller, and a edit object actuator
in the edit object actuator set the type to replace mesh and type in the mesh to use for the visualization and make sure Gfx and Phys are both checked
use delay actuator instead - always runs it constantly and runs logic time way up


moving the cg lower on the vehicle prevents popping up when starting
using box collision constraint with lowered cg causes box to drag the ground

Setup of the robot file 
-----------------------

Launch MORSE by typing ``morse``, and erase all objects in the file:

#. Press :kbd:`a` to select all
#. Press :kbd:`x` and :kbd:`enter` to delete

Save the file with a name that represents the the robot. As an
example this document will use the Ressac helicopter, so the name of the file
should be something like::

``$MORSE_ROOT/share/data/morse/components/robots/myrobot_equiped.blend``

#. Press :kbd:`F2` to open the ``Save as`` dialog
#. Navigate to the correct path and type the name of the file
#. Press the **Save File** button

Next link in the base of the robot from the component library:

#. With the mouse over the 3D view in Blender, press :kbd:`Ctrl-Alt-O` to open the Load Library browser
#. Navigate to the directory ``$MORSE_ROOT/data/morse/components/robots``
#. Press :kbd:`Left Mouse Click` over the file ``ressac.blend``
#. Press :kbd:`Left Mouse Click` over the item ``Object``
#. Press :kbd:`Right Mouse Click` and drag over the names of all the objects listed, to select them all
#. Press the button **Link/Append from Library**. You'll return to the 3D View, and the newly added
   human is selected, but can not move around.
#. Convert the objects to local: without de-selecting the object, press :kbd:`l` then hit :kbd:`enter`
#. If you deselected the inserted objects in the scene, select it again either by 
   :kbd:`Right Mouse Click` clicking over the object in the 3D View, or 
   :kbd:`Left Mouse Click` over the object's name in the Outliner window. The object 
   will be highlighted in cyan colour.
#. Select as well the child objects, by pressing :kbd:`Shift-g`, then hitting :kbd:`enter`

The rest of the components (sensors and actuators) should be linked similarly.
Refer to the :doc:`Quick tutorial <../tutorial>` for instructions. In the
case of a robot file, no middlewares or modifiers should be added, since those
would be specific to every particular scenario.

Adjust the properties of the component if necessary. Then save the file again,
by pressing :kbd:`Ctrl-w`, followed by :kbd:`enter`.

This robot file should be liked into scenarii files by following the same
procedure, while selecting all the objects contained in the file.

