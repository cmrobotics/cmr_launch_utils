from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from cmr_launch_utils.substitutions import PackageShareDirectorySubstitution, IfElseSubstitution, TextFormatSubstitution


def generate_launch_description():
    # Launch substitutions
    root_is_ros_package = LaunchConfiguration("root_is_ros_package")

    package_root_directory = IfElseSubstitution(
        condition=IfCondition(root_is_ros_package),
        if_true=PackageShareDirectorySubstitution(
            LaunchConfiguration("package_root_directory")
        ),
        if_false=LaunchConfiguration("package_root_directory"),
    )

    model_name = LaunchConfiguration("model_name")

    model_file = PathJoinSubstitution(
        substitutions=[
            package_root_directory,
            "models",
            model_name,
            TextFormatSubstitution(
                fmt="model.{}",
                substitutions=[LaunchConfiguration("file_extension")]
            )
        ]
    )

    entity_name = LaunchConfiguration(
        "entity_name",
        default=model_name
    )

    pose_x = LaunchConfiguration("pose_x")
    pose_y = LaunchConfiguration("pose_y")
    pose_yaw = LaunchConfiguration("pose_yaw")

    namespace = LaunchConfiguration("namespace")

    # Declare the launch actions
    file_extension_action = DeclareLaunchArgument(
        "file_extension",
        default_value="urdf",
        description="Extension of the model file"
    )

    namespace_action = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace to use for the ROS interfaces created for the entity (e.g., topics)"
    )

    root_is_ros_package_action = DeclareLaunchArgument(
        "root_is_ros_package",
        default_value="True",
        description="Set to True if the \"package_root_directory\" is the name of a ROS package. Otherwise, set to False when passing a full path"
    )

    package_root_directory_action = DeclareLaunchArgument(
        "package_root_directory",
        description="The package name when \"root_is_ros_package\" is True, otherwise the full path the root directory with the models"
    )

    model_name_action = DeclareLaunchArgument(
        "model_name",
        description="The name of the model such that the model description is found at \"root_is_ros_package\"/models/\"model_name\"/model.sdf"
    )

    entity_name_action = DeclareLaunchArgument(
        "entity_name",
        description="Name given to the entity when spawning it in Gazebo; defaults to the model's name",
        default_value=model_name
    )

    x_arg_action = DeclareLaunchArgument(
        "pose_x",
        default_value="0.0",
        description="The position to spawn the model on the x axis"
    )

    y_arg_action = DeclareLaunchArgument(
        "pose_y",
        default_value="0.0",
        description="The position to spawn the model on the y axis"
    )

    yaw_arg_action = DeclareLaunchArgument(
        "pose_yaw",
        default_value="0.0",
        description="The angle to spawn the model around the z axis (yaw angle)"
    )

    spawn_entity_action = Node(
        package="gazebo_ros",
        executable='spawn_entity.py',
        arguments=[
            "-entity", entity_name,
            "-file", model_file,
            "-robot_namespace", namespace,
            "-x", pose_x,
            "-y", pose_y,
            "-z", "0.2",
            "-Y", pose_yaw
        ],
        output="screen",
    )


    # Create launch description object
    ld = LaunchDescription()

    # Register launch actions for finding the model
    ld.add_action(file_extension_action)
    ld.add_action(namespace_action)
    ld.add_action(root_is_ros_package_action)
    ld.add_action(package_root_directory_action)
    ld.add_action(model_name_action)

    # Register launch actions related to the model's pose
    ld.add_action(x_arg_action)
    ld.add_action(y_arg_action)
    ld.add_action(yaw_arg_action)

    # Launch actions to run things
    ld.add_action(spawn_entity_action)

    return ld
