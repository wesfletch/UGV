cmake_minimum_required(VERSION 3.5)
project(ugv_sim)

# Default C version to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default C++ version to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# build with all warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)

ament_python_install_package(${PROJECT_NAME})

# install launch files
install(DIRECTORY
  launch
  worlds
  meshes
  rviz
  models
  DESTINATION share/${PROJECT_NAME}/
)

# install python scripts
# install(DIRECTORY 
#   scripts/
#   DESTINATION lib/${PROJECT_NAME}
# )

install(PROGRAMS  # PROGRAMS is just like FILES, but gives 'execute' permissions to installed targets
  scripts/motors.py
  DESTINATION lib/${PROJECT_NAME}
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
