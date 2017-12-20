#!/bin/bash
[[ $- != *i* ]] && exit

if [ -f $HOME/catkinws/devel/setup.bash ]; then
	source $HOME/catkinws/devel/setup.bash
elif [ -f /opt/ros/kinetic/setup.bash ]; then
	echo "couldn't find catkin workspace '$HOME/catkinws'!"
	echo sourcing '/opt/ros/kinetic/setup.bash' instead!
	source /opt/ros/kinetic/setup.bash
else
	echo no existing ROS installation found!!!
	echo Please contact administrator of TurtleBot robot
fi

export ROS_MASTER_URI=http://htb-b1:11311

