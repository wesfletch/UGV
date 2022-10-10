from ast import arg
import os
import sys

from ament_index_python import get_package_share_directory

from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, FindExecutable
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # launch args
    arg_robot_name = DeclareLaunchArgument(
        "robot_name",
        description="The name of the robot to be launched. Will be used to match model name and namespace simulation outputs.",
        default_value="choo_2",
    )
    arg_description_package = DeclareLaunchArgument(
        "description_package",
        description="The ROS package that contains the robot description (.urdf and .xacro files).",
        default_value="ugv_description",
    )
    arg_world_file = DeclareLaunchArgument(
        "world_file",
        description="Gazebo world file to launch Gazebo with.",
        default_value=os.path.join(get_package_share_directory('ugv_sim'), 'worlds', 'course.world')
    )
    arg_rviz = DeclareLaunchArgument(
        "rviz",
        description="[true/false] Launch RVIZ window with rviz_cfg as config file. Default false.",
        default_value='false',
    )
    arg_rviz_cfg = DeclareLaunchArgument(
        "rviz_cfg",
        description="RVIZ cfg file (.rviz) to launch RVIZ with.",
        default_value=os.path.join(get_package_share_directory('ugv_sim'), 'rviz', 'bowser2.rviz'),
    )
    
    # sim.launch brings up the robot_description and all sensor inputs
    include_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('ugv_sim'), "launch", "sim.launch.py"])),
        launch_arguments={
            'robot_name': LaunchConfiguration('robot_name'),
            'description_package': LaunchConfiguration('description_package'),
            'world_file': LaunchConfiguration('world_file'),
            'gaz_client': 'true',
            'rviz': LaunchConfiguration('rviz'),
            'rviz_cfg': LaunchConfiguration('rviz_cfg'),
        }.items(),
    )

    include_nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('ugv_nav'), "launch", "nav.launch.py"])),
        launch_arguments={
            'use_sim_time': 'true',
        }.items(),
    )
    
    return LaunchDescription([
        arg_robot_name,
        arg_description_package,
        arg_world_file,
        arg_rviz,
        arg_rviz_cfg,

        include_sim_launch,
        include_nav_launch,
    ])