import os, sys, subprocess

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, TextSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue

def generate_launch_description():

    # CLI args for configuring nodes, since apparently ROS doesn't allow substitutions inside default values
    # set defaults
    robot_name = "choo_2"
    robot_desc_file = os.path.join(get_package_share_directory('ugv_description'),
                                   'urdf', robot_name, 'model.urdf.xacro')
    world_file_path = os.path.join(get_package_share_directory('ugv_sim'),
                                   'worlds','course.world')
    rviz_cfg_file = os.path.join(get_package_share_directory('ugv_sim'),
                                 'rviz','bowser2.rviz')
    # read in sys args that we need before launch-time by pretending they're normal launch args
    for arg in sys.argv:       
        if arg.startswith("robot:="):
            robot_name = arg.split(":=")[1]
        elif arg.startswith("robot_desc_file:="):
            robot_desc_file = arg.split(":=")[1]
        elif arg.startswith("world_file:="):
            world_file_path = arg.split(":=")[1]
        elif arg.startswith("rviz_cfg:="):
            rviz_cfg_file = arg.split(":=")[1]

    # normal launch args
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
    arg_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        description="[true/false] Whether nodes launched by this file should use sim time (as opposed to wall time).",
        default_value='true',
    )

    # launch gzserver
    gazebo_launch_file = os.path.join(get_package_share_directory('gazebo_ros'),
                                      'launch/',
                                      'gzserver.launch.py')
    include_launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'verbose':'true',
            'paused':'false',
            'world':world_file_path,
        }.items()
    )

    # generate robot description (URDF) by processing model.urdf.xacro
    robot_desc_path = os.path.dirname(robot_desc_file)
    robot_desc_urdf_path = os.path.join(robot_desc_path, 'model.urdf')
    # load robot URDF by expanding our xacro definition (with the xacro command)
    with open(robot_desc_urdf_path, 'w') as urdf_file:
        xacro_cmd = subprocess.run(['xacro', '-v', robot_desc_file], 
                                   stdout=urdf_file, 
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
    with open(robot_desc_urdf_path, 'r') as infp:
        robot_desc_urdf = infp.read()
        
    # robot_state_publisher (load with xacro expanded to URDF)
    node_robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        # output="screen",
        parameters=[{
            'use_sim_time':LaunchConfiguration('use_sim_time'),
            'robot_description':robot_desc_urdf,
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
            '-file', robot_desc_urdf_path,
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
    )

    return LaunchDescription([
        # arg_world_file,
        arg_gaz_client,
        arg_rviz,
        # arg_rviz_cfg_file,
        arg_use_sim_time,
        include_launch_gazebo,
        node_spawn_robot,
        node_robot_state_pub,
        node_joint_state_pub,
        node_rviz,
    ])