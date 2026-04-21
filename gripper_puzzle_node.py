#!/usr/bin/env python3
# gripper puzzle node.py
# 
# Incorporates: MoveIt2, wrappers (pymoveit2)
# Sources: modified from pymoveit2 source code example on gripper action

from threading import Thread
import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

from pymoveit2 import GripperInterface
from pymoveit2.robots import panda as robot

class PuzzlePieceGripperNode(Node):
    def __init__(self):
        super().__init__("puzzle_piece_gripper_node")

        # callback group
        self.callback_group = ReentrantCallbackGroup()

        # gripper interface
        self.gripper_interface = GripperInterface(
            node=self,
            gripper_joint_names=robot.gripper_joint_names(),
            open_gripper_joint_positions=robot.OPEN_GRIPPER_JOINT_POSITIONS,
            closed_gripper_joint_positions=robot.CLOSED_GRIPPER_JOINT_POSITIONS,
            gripper_group_name=robot.MOVE_GROUP_GRIPPER,
            callback_group=self.callback_group,
            gripper_command_action_name="gripper_action_controller/gripper_cmd",
        )

    # 
    def open_gripper(self):

        #self.get_logger().info("opening gripper...")
        self.gripper_interface.open()
        self.gripper_interface.wait_until_executed()
        #self.get_logger().info("gripper opened")

    def close_gripper(self):

        # self.get_logger().info("Closing gripper on puzzle piece...")
        self.gripper_interface.close()
        self.gripper_interface.wait_until_executed()
        # self.get_logger().info("gripper closed")

    def gripper_puzzle_piece(self):
        """
        This only handles the gripper part of pickup...
        The arm motion should happen before/after these calls.
        """

        # Step 1: open before approaching piece
        self.open_gripper()

        # Step 2: arm should move to grasp pose here
        self.get_logger().info("TODO: Move arm to puzzle piece grasp pose.")
        time.sleep(1.0)  # supposed to calculate where the piece is

        # Step 3: close gripper to grasp piece
        # once it gets there
        self.close_gripper()

        # Step 4: arm should lift piece here
        self.get_logger().info("TODO: Lift puzzle piece.")
        time.sleep(1.0)  # placeholder


def main():
    rclpy.init()

    node = PuzzlePieceGripperNode()

    # apprently it spins the node in background threads and wait til execution
    executor = rclpy.executors.MultiThreadedExecutor(2)
    executor.add_node(node)
    executor_thread = Thread(target=executor.spin, daemon=True)
    executor_thread.start()
    node.create_rate(1.0).sleep()

    # from the source code doc: sleep a while to get first joint state
    node.create_rate(10.0).sleep()

    # run test pickup sequence
    node.pick_up_puzzle_piece()

    rclpy.shutdown()
    executor_thread.join()
    exit(0)


if __name__ == "__main__":
    main()