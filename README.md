# hiwonder_xArm_1s

![alt text](https://github.com/KaburaJ/hiwonder_xArm_1s/blob/main/image.png)

<br>
The Hiwonder xArm 1s (found here https://www.hiwonder.com/products/xarm-1s?variant=32436121894999) is a 6 D.O.F Aluminium 0.9 kg robotic arm with Bluetooth and USB communication capabilities.

How to run:

For Ubuntu or Raspberry Pi running on Ubuntu OS users:

## Requirements
```
git clone https://github.com/KaburaJ/hiwonder_xArm_1s.git
```

**Something to note is that if you encounter errors while trying to connect to the arm, try adding the following udev rule to `/etc/udev/rules.d/99-xarm.rules` using the command `sudo nano /etc/udev/rules.d/99-xarm.rules`:**
```
SUBSYSTEM=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="5750", MODE="0660", GROUP="plugdev"
```
**Then reload the rules with:**
```
sudo udevadm control --reload-rules 
sudo udevadm trigger
```

**Where you choose to add the rules above, please run the command below to add your root to the `plugdev` group.**
```
sudo usermod -aG plugdev $USER
```

These steps will allow users in the plugdev group to access the arm controller.
## Packages
| Name | Description | 
|----------|----------|
| learm_ros2   | A simple follower that commands arm servo positions from joint states published on the joint_states topic.   | 
| learm_ros2_description    | LeArm description files, including arm meshes and URDF files.  |
| learm_ros2_moveit_config   | MoveIt config files (WIP).  |

## Running
1. Run `sudo -s` on your terminal. The assumption is that you've already installed ROS2.
1. Run to install the required packages:
```
sudo apt-get install libusb-1.0-0-dev libudev-dev
pip install --upgrade setuptools
pip install hidapi
pip install xarm 
```
1. Change directories to the location of the project you cloned above.
1. Run ```source /opt/ros/$DISTRO/setup.bash```. Remember to always do this whenever you open a new terminal.
1. Run ```colcon build```
1. Next, ```source install/setup.bash```
1. And, ```ros2 launch learm_ros2 follower.launch.py```. Make sure the robotic arm is plugged into a power source, turned on, and connected over USB. Then start this follower launch file.

In another terminal, repeat steps 1, 2 and 4 respectively before running:
```
ros2 launch learm_ros2 follower.launch.py
```

Use the joint state publisher interface to move the robot on rviz2 as well as the physical. You should get the response as in the video below.

## Demo
Accessible here https://youtu.be/bHPxp2J4lWQ?si=cHmpUlG4LA_Bw6Jf




