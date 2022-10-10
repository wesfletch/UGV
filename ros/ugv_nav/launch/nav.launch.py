import os
import sys

from ament_index_python import get_package_share_directory

from launch import LaunchDescription, LaunchContext
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def launch_setup(context: LaunchContext, *foo, **bar):

    pass

def generate_launch_description():

    # set defaults
    default_params_file = os.path.join(get_package_share_directory("ugv_nav"),
                                       'config', 'nav2_params.yaml')

    arg_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock',
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    arg_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=default_params_file,
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node'
    )
    params_file = LaunchConfiguration('params_file')

    # Since slam_toolbox requires a LaserScan, and we don't have a planar lidar,
    #   we'll use this to down-project a 3D pointcloud to a 2D laser scan.
    node_pointcloud_to_laserscan = Node(
        package="pointcloud_to_laserscan",
        executable="pointcloud_to_laserscan_node",
        name="pointcloud_to_laserscan",
        output="screen",
        parameters=[
            params_file,
        ],
        remappings=[
            ('cloud_in','/choo_2/velodyne_points'),
        ],
        arguments=['--ros-args', '--log-level', 'debug']
    )

    node_slam_toolbox = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="async_slam_toolbox",
        output="screen",
        parameters=[
            params_file,
            {'use_sim_time': use_sim_time},
        ]
    )

    return LaunchDescription([
        arg_use_sim_time,
        arg_params_file,
        node_pointcloud_to_laserscan,
        node_slam_toolbox,
    ])