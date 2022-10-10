#!/usr/bin/env python3

"""Allows teleoperation of a simulation vehicle with the arrow keys.

Assumes differential drive control. Publishes geometry_msg/Twist messages on the provided topic.
"""

import sys
from typing import Dict, List

from pynput import keyboard

import rclpy
from rclpy.node import Node
import geometry_msgs.msg as geom


class MotorsPub(rclpy.node.Node):

    def __init__(self, topic: str = '/cmd_vel', freq: int = 50, speeds: List[float] = [1.2,-1.2,-1.2,1.2]) -> None:
        """A ROS2 node that publishes motor commmands on provided topic at provided freq based on keyboard inputs.
        
        Intended to control differential drive vehicles (in sim, mostly).

        Args:
            topic (str, optional): The topic to publish geometry_msgs/Twist messages on. Defaults to '/cmd_vel'.
            freq (int, optional): Frequenct to publish messages at. Defaults to 50.
            speeds (List[float], optional): List of motor speeds. Format is [FWD,REV,CW,CCW]. Defaults to [1.2,-1.2,1.2,-1.2].
        """

        super().__init__(node_name='motor_publisher')
        
        self.publisher: rclpy.Publisher = self.create_publisher(
            msg_type=geom.Twist, 
            topic=topic, 
            qos_profile=10)
        
        self.speeds: Dict[str, float] = {
            'FORWARD': speeds[0],
            'REVERSE': speeds[1],
            'CW'     : speeds[2],
            'CCW'    : speeds[3],
        }

        # message to be published
        self.twist: geom.Twist = geom.Twist()
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = 0.0

        # timer that fires at provided frequency
        self._timer_period: float = 1 / freq
        self.timer: rclpy.Timer = self.create_timer(self._timer_period, self.timer_callback)

        # listener for keyboard press/release events
        self.listener: keyboard.Listener = keyboard.Listener(
            on_press=self.on_press_cb,
            on_release=self.on_release_cb)
        self.listener.start()

    def timer_callback(self) -> None:
        """Publishes the Twist message created by listening to keyboard inputs.

        Fires at the frequency provided to the constructor.
        """

        self.publisher.publish(self.twist)
        
    def on_press_cb(self, key: keyboard.Key) -> bool:
        """When a key is pressed, modify the Twist message that is published by this node.

        Args:
            key (keyboard.Key): The key code that caused this callback to fire.

        Returns:
            bool: Returns false to stop listener (when ESC is pressed)
        """

        # If ESC is pressed, exits keyboard listener
        if key == keyboard.Key.esc:
            # Stop listener
            return False     

        try:
            k = key.char
        except AttributeError:
            k = key.name

        # Modifies twist message depending on which arrow key event we captured.
        # TODO: uses IF rather than ELIF, can multiple keys be captured in a single callback?    
        if k == 'left':
            self.twist.angular.z = self.speeds['CCW']
        if k == 'right':
            self.twist.angular.z = self.speeds['CW']
        if k == 'up':
            self.twist.linear.x = self.speeds['FORWARD']
        if k == 'down':
            self.twist.linear.x = self.speeds['REVERSE']

        return True     # True keeps keyboard listener running.

    def on_release_cb(self, key: keyboard.Key) -> None:
        """When a key is released, zero that key out in the Twist message

        Args:
            key (keyboard.Key): The key code that caused this callback to fire.
        """

        try:
            k = key.char
        except AttributeError:
            k = key.name

        # zero out the field of whatever key was released    
        if k == 'left':
            self.twist.angular.z = 0.0
        if k == 'right':
            self.twist.angular.z = 0.0
        if k == 'up':
            self.twist.linear.x = 0.0
        if k == 'down':
            self.twist.linear.x = 0.0  

def main():

    rclpy.init(args=sys.argv) 

    motors_pub = MotorsPub()
    rclpy.spin(motors_pub)    # keeps this ros node from closing
    
    rclpy.shutdown()

if __name__=='__main__':
    main()
