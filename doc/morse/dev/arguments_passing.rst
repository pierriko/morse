How arguments are passed between builder and the simulator ?
============================================================

There are lots of information expressed in Builder script that are not
directly translatable in blender model. Here, we describe how the information
are passed between the builder script and the simulator.

Properties
----------

Some information are passed directly through the *game engine property* of
each component. It includes stuff like **classpath** (what python class
implements the logic of this component) or components properties (passed using
the :py:meth:`morse.builder.abstractcomponent.AbstractComponent.properties`
method).

However, passing information through *game engine properties* has some
limitations: it must be one of basic type (string, int, double, ...), and the
range on int and double is limited by Blender. It is not good enough to
translate more complex informations.

The component_config.py file
----------------------------

Information concerning scene configuration (i.e. which datastream handler for
which component, which service for which component, ...) are passed through
the file ``component_config.py``  stored in the blender scene. You can
retrieve it using the **Text Editor** window in Blender.

This file contains a relatively complex python structure, encoding the
configuration for the different part mentioned above. The file is
automatically generated by the Builder using the method
:py:meth:`morse.builder.abstractcomponent.Configuration.write_config`. On the
simulator side, the file is imported in :py:mod:`morse.blender.main`, and used
to create the different internal structures (see :doc:`entry_point`).

More precisely, the file contains five dictionaries:

- ``component_datastream`` contains for each component the list of associated
  datastream handler. Each datastream handler is defined by a list of three
  elements:

  #. the datastream manager
  #. the specific datastream handler class
  #. a dictionary containing extra arguments for the datastream handler

- ``component_modifier`` contains for each component the list of associated
  modifiers Each modifier is defined by a list of three elements:

  #. Its class
  #. the method name in the class
  #. a dictionary containing extra arguments for the modifier class

- ``component_service`` contains for each component the list of associated
  service handler defined by its classpath.

- ``overlays`` contains for each service handler and for component
  the list of associated overlays represented by their classpath.

- ``stream_manager`` contains for each stream manager a list of options passed
  to this specific stream manager.

Example
+++++++
The scene
_________


.. code-block:: python

    from morse.builder import *

    robot = ATRV()

    pose = Pose()
    pose.add_stream('socket')
    pose.alter('Noise')
    robot.append(pose)

    odometry = Odometry()
    odometry.level("differential")
    odometry.add_stream('socket')
    robot.append(odometry)

    waypoint = Waypoint()
    waypoint.add_interface('socket')
    robot.append(waypoint)

    env = Environment('empty', fastmode=True)
    env.configure_stream_manager('socket', time_sync = True, sync_port = 5000)


Generated component_config.py
_____________________________

.. code-block:: python

    component_datastream = {'robot.odometry':
        [['morse.middleware.socket_datastream.SocketDatastreamManager',
            'morse.middleware.socket_datastream.SocketPublisher',
            {}]],
    'robot.pose':
                [['morse.middleware.socket_datastream.SocketDatastreamManager',
                 'morse.middleware.socket_datastream.SocketPublisher',
                {}]],
    'robot.waypoint':
                [['morse.middleware.socket_datastream.SocketDatastreamManager',
                'morse.middleware.socket_datastream.SocketReader',
                {}]]}
    component_modifier = {'robot.pose': [['morse.modifiers.pose_noise.PoseNoiseModifier', {}]]}
    component_service = {'robot.waypoint': ['morse.middleware.socket_request_manager.SocketRequestManager']}
    overlays = {}
    stream_manager = {'morse.middleware.socket_datastream.SocketDatastreamManager': {'sync_port': 5000,
                                                                                     'time_sync': True}}
