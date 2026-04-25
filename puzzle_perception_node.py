#!/usr/bin/env python3

# description: perception

import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import Bool, String
from cv_bridge import CvBridge

class PuzzlePerceptionNode(Node):
    def __init__(self):
        super().__init__("puzzle_piece_perception_node")

        self.bridge = CvBridge()

        self.image_subscriber = self.create_subscription(
            Image,
            "/camera/image_raw",
            self.image_callback,
            1,
        )

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        # detected = detect_piece(frame)
      
    
    def detect_piece(self, frame):
        '''
        placeholder function
        '''
        pass