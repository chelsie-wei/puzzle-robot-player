#!/usr/bin/env python3

# webcam node
# Description: webcam
# TODO: 

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class WebCameraNode(Node):
    def __init__(self):
        super().__init__("webcam_camera_node")

        self.publisher = self.create_publisher(Image, "/camera/image_raw", 1)
        self.bridge = CvBridge()
        self.capture = cv2.VideoCapture(0)

        self.timer = self.create_timer(0.1, self.publish_frame)
        self.get_logger().info("Starting webcam")

    def publish_frame(self):
        r, f = self.capture.read()

        msg = self.bridge.cv2_to_imgmsg(f, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "cam_frame"

        self.publisher.publish(msg)