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
from launch.conditions import IfCondition

def launch_setup(context: LaunchContext, *foo, **bar):

    description_package = LaunchConfiguration("description_package")
    robot_name          = LaunchConfiguration("robot_name")
    world_file          = LaunchConfiguration("world_file")
    rviz_cfg_file       = LaunchConfiguration("rviz_cfg")
    arg_rviz            = LaunchConfiguration("rviz")

    # generate robot description (URDF) by processing model.urdf.xacro with the 'xacro ...' command
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare(description_package), "urdf", robot_name, "model.urdf.xacro"]),
        ]
    )

    # launch gzserver
    gazebo_launch_file = os.path.join(get_package_share_directory('gazebo_ros'),
                                      'launch/',
                                      'gzserver.launch.py')
    include_launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'verbose': 'true',
            'paused': 'false',
            'world': world_file,
        }.items()
    )

    # robot_state_publisher (load with xacro expanded to URDF)
    node_robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        # output="screen",
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': ParameterValue(value=robot_description_content, value_type=str), # explicit str to stop it trying to parse the xml
        }],
        # arguments=['--ros-args', '--log-level', 'debug'],
    )

    # spawn robot into our gazebo world
    node_spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_entity",
        output="screen",
        arguments=[
            '-topic', '/robot_description',     # use output of robot_state_publisher to spawn robot
            '-entity', robot_name, 
        ]
    )

    # joint state publisher
    node_joint_state_pub = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        output="screen", 
    )

    # rviz2
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz",
        arguments=['-d', rviz_cfg_file],
        condition=IfCondition(arg_rviz),
    )

    nodes_to_start = [
        include_launch_gazebo, 
        node_robot_state_pub, 
        node_spawn_robot,
        node_joint_state_pub,
        node_rviz, 
    ]

    return nodes_to_start

def generate_launch_description():

    # launch args
    arg_robot_name = DeclareLaunchArgument(
        "robot_name",
        description="The name of the robot to be launched. Will be used to match model name and namespace simulation outputs.",
        default_value="choo_2",
    )
    arg_world_file = DeclareLaunchArgument(
        "world_file",
        description="Gazebo world file to launch Gazebo with.",
        default_value=os.path.join(get_package_share_directory('ugv_sim'), 'worlds', 'course.world')
    )
    arg_description_package = DeclareLaunchArgument(
        "description_package",
        description="The ROS package that contains the robot description (.urdf and .xacro files).",
        default_value="ugv_description",
    )
    arg_gaz_client = DeclareLaunchArgument(
        "gaz_client",
        description="[true/false] Launch the full Gazebo GUI (gzclient). Default false.",
        default_value='false',
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
    arg_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        description="[true/false] Whether nodes launched by this file should use sim time (as opposed to wall time).",
        default_value='true',
    )

    return LaunchDescription([
        arg_robot_name,
        arg_world_file,
        arg_description_package,
        arg_gaz_client,
        arg_rviz,
        arg_rviz_cfg,
        arg_use_sim_time,

        # We set up Nodes and Commands that require the values in launch args in a separate function,
        #   since we don't have access to them until AFTER get_launch_description() returns (without extensive hackery).
        #   OpaqueFunction allows us to add that separate function to the launch description to be executed later.
        OpaqueFunction(function=launch_setup),
    ])