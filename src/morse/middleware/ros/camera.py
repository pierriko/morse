import logging; logger = logging.getLogger("morse." + __name__)
import roslib; roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    component_instance.output_functions.append(function)
    self.register_publisher_name_class(self.get_topic_name() + "/image", Image)
    self.register_publisher_name_class(self.get_topic_name() + "/camera_info", CameraInfo)

    logger.info('ROS publisher for %s initialized'%component_instance.name())

def post_image(self, component_instance):
    """ Publish the data of the Camera as a ROS Image message.

    """
    if not component_instance.capturing:
        return # press [Space] key to enable capturing

    image = Image()
    image.header = self.get_ros_header(component_instance)
    image.header.frame_id += '/base_image'
    image.height = component_instance.image_height
    image.width = component_instance.image_width
    image.encoding = 'rgba8'
    image.step = image.width * 4
    # NOTE: Blender returns the image as a binary string encoded as RGBA
    # sensor_msgs.msg.Image.image need to be len() friendly
    # TODO patch ros-py3/common_msgs/sensor_msgs/src/sensor_msgs/msg/_Image.py
    # to be C-PyBuffer "aware" ? http://docs.python.org/c-api/buffer.html
    image.data = bytes(image_local.image)
    # http://wiki.blender.org/index.php/Dev:Source/GameEngine/2.49/VideoTexture
    # http://www.blender.org/documentation/blender_python_api_2_57_release/bge.types.html#bge.types.KX_Camera.useViewport

    # sensor_msgs/CameraInfo [ http://ros.org/wiki/rviz/DisplayTypes/Camera ]
    # fill this 3 parameters to get correcty image with stereo camera
    Tx = 0
    Ty = 0
    R = [1, 0, 0, 0, 1, 0, 0, 0, 1]

    intrinsic = component_instance.local_data['intrinsic_matrix']

    camera_info = CameraInfo()
    camera_info.header = image.header
    camera_info.height = image.height
    camera_info.width = image.width
    camera_info.distortion_model = 'plumb_bob'
    camera_info.K = [intrinsic[0][0], intrinsic[0][1], intrinsic[0][2],
                     intrinsic[1][0], intrinsic[1][1], intrinsic[1][2],
                     intrinsic[2][0], intrinsic[2][1], intrinsic[2][2]]
    camera_info.R = R
    camera_info.P = [intrinsic[0][0], intrinsic[0][1], intrinsic[0][2], Tx,
                     intrinsic[1][0], intrinsic[1][1], intrinsic[1][2], Ty,
                     intrinsic[2][0], intrinsic[2][1], intrinsic[2][2], 0]

    self.publish_topic(image, self.get_topic_name(component_instance) + "/image")
    self.publish_topic(camera_info, self.get_topic_name(component_instance) + "/camera_info")
