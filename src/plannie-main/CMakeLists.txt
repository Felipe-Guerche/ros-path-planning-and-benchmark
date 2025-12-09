cmake_minimum_required(VERSION 3.0.2)
project(plannie)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  nav_msgs
  actionlib
  move_base_msgs
)

catkin_package(
  CATKIN_DEPENDS
    rospy
    std_msgs
    geometry_msgs
    nav_msgs
    actionlib
    move_base_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  movimentoROS.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
