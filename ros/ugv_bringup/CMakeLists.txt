cmake_minimum_required(VERSION 3.5)
project(ugv_bringup)

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
# find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)

# ament_python_install_package(${PROJECT_NAME})

# install data files
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
)

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
