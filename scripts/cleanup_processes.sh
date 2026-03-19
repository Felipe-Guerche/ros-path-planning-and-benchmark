#!/bin/bash
# Kill all ROS/Gazebo processes between benchmark runs
killall -9 rosmaster 2>/dev/null || true
killall -9 roscore 2>/dev/null || true
killall -9 roslaunch 2>/dev/null || true
killall -9 rosout 2>/dev/null || true
killall -9 move_base 2>/dev/null || true
killall -9 rviz 2>/dev/null || true
killall -9 gzserver 2>/dev/null || true
killall -9 gzclient 2>/dev/null || true
killall -9 robot_state_publisher 2>/dev/null || true
killall -9 amcl 2>/dev/null || true
killall -9 map_server 2>/dev/null || true
# killall -9 Xvfb 2>/dev/null  # DO NOT KILL XVFB (Entrypoint manages it)
