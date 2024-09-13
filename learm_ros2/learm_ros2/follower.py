#!/usr/bin/env python

import rclpy
from sensor_msgs.msg import JointState
import xarm
import sys

try:
    # Use serial.Serial() instead of serial()
    # ser = serial.Serial(port="USB", baudrate=115200, timeout=10000)
    # print(ser)
    print("shtukaaaa")
    arm = xarm.Controller("USB", debug=True)
    print("sishtukiiiii")
except OSError as e:
    print("Failed to connect to Robot", e)
    sys.exit(1)


print('Battery voltage in volts:', arm.getBatteryVoltage())

# Initialize with invalid value so first received coordinate gets sent to robot
# FUTURE: read the current robot position from controller and update memory state
servos = {
    "shoulder_pan": xarm.Servo(6, 500),
    "shoulder_lift": xarm.Servo(5, 500),
    "elbow": xarm.Servo(4, 500),
    "wrist_flex": xarm.Servo(3, 500),
    "wrist_roll": xarm.Servo(2, 500),
    "grip_right": xarm.Servo(1, 500),  # Flipped in URDF (open is close)
}

def recv_sensorMsgs_jointState(jointState):
    changed = False
    # rclpy.logging.get_logger('follower').info('Received: ' + str({n: p for n, p in zip(jointState.name, jointState.position)}))

    for name, position in zip(jointState.name, jointState.position):
        # Check if we know how to control this joint
        servo = servos.get(name, None)
        if not servo:
            continue

        # Convert desired position to robot coordinates
        value = position  # radians [-1.57, 1.57]
        value /= 1.57  # convert [-1, 1]
        value *= 500  # convert [-500, 500]
        value += 500  # convert [0, 1000]
        value = int(value)  # truncate decimals so library operates correctly

        # Update the desired position in memory
        if servo.position != value:
            servo.position = value
            changed = True

    # If anything updated, notify the hardware
    if changed:
        # rclpy.logging.get_logger('follower').info('Sending: ' + str({n: s.position for n, s in servos.items()}))
        arm.setPosition(list(servos.values()), duration=1)


def main():
    # TODO: include robot serial code in topic
    rclpy.init(args=sys.argv)
    node = rclpy.create_node('follower')
    node.get_logger().info('Created node')

    sub = node.create_subscription(JointState, 'joint_states', recv_sensorMsgs_jointState, 10)
    
    rclpy.spin(node)


if __name__ == '__main__':
    main()

