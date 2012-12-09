import roslib; roslib.load_manifest('sensor_msgs')
from std_msgs.msg import Header
from sensor_msgs.msg import PointCloud2

from morse.middleware.ros import point_cloud2

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    self.register_publisher(component_instance, function, PointCloud2)

def post_pointcloud2(self, component_instance):
    """ Publish the data of the Depth Camera as a ROS PointCloud2 message.

    """
    if not component_instance.capturing:
        return # press [Space] key to enable capturing

    header = self.get_ros_header(component_instance)

    points = component_instance.local_data['3D_points']
    pc2 = point_cloud2.create_cloud_xyz32(header, points,
                                          component_instance.image_width *
                                          component_instance.image_height)

    self.publish(pc2, component_instance)
