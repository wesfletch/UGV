cmake_minimum_required(VERSION 3.5)
project(ugv_nav)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)
find_package(robot_localization REQUIRED)
find_package(slam_toolbox REQUIRED)

install(DIRECTORY 
  config
  launch
  DESTINATION share/${PROJECT_NAME}/)

ament_export_include_directories(
  # replaces INCLUDE_DIRS
)
ament_export_libraries(
  # replaces LIBRARIES
)
ament_export_dependencies(
  # replaces CATKIN_DEPENDS
)
ament_package(
  # EXTRA_CONFIGS XX XX XX
)
