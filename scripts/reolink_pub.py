#!/usr/bin/env python3

# Import the necessary libraries

camera_link = 'rtsp://admin:ieeeras@192.168.1.223:554/h264Preview_01_main'
print(camera_link)

import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library

class reolink():
    import rospy  # Python library for ROS
    from sensor_msgs.msg import Image  # Image is the message type
    from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
    import cv2  # OpenCV library

    def __init__(self):

        # Node is publishing to the video_frames topic using
        # the message type Image
        self.pub = rospy.Publisher('video_frames', Image, queue_size=10)

        # Tells rospy the name of the node.
        # Anonymous = True makes sure the node has a unique name. Random
        # numbers are added to the end of the name.
        self.rospy.init_node('video_pub_py', anonymous=True)

        # Go through the loop 10 times per second
        self.rate = rospy.Rate(30)  # 10hz

        # Create a VideoCapture object
        # The argument '0' gets the ip camera.
        self.camera_link = camera_link
        # cap = cv2.VideoCapture(camera_link)

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()
        try:
            self.cap = cv2.VideoCapture(camera_link)
            self.width = 0
            self.height = 0

            if self.cap.isOpened():
                self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print('Reolink camera connected  width= ', self.width, ', height= ', self.height)
            else:
                print('failed to open the camera for streaming')
        except:
            print('exception - debug')


    def rescale_frame(self, frame, percent=25):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)

        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def capture(self):
        self.cnt = 0

        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            resized_frame = self.rescale_frame(frame, percent=25)

            if ret == True:

                self.pub.publish(self.br.cv2_to_imgmsg(resized_frame))

            self.rate.sleep()

if __name__ == '__main__':
  try:
      camObj = reolink()
      camObj.capture()
  except rospy.ROSInterruptException:
    pass
