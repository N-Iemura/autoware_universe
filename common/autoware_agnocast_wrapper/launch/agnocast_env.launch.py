from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import SetLaunchConfiguration
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch.substitutions import EnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression


def generate_launch_description():
    use_agnocast = SetLaunchConfiguration(
        "use_agnocast", EnvironmentVariable("ENABLE_AGNOCAST", default_value="0")
    )

    set_container_package_default = SetLaunchConfiguration(
        "container_package",
        "rclcpp_components",
        condition=UnlessCondition(
            PythonExpression(["'", LaunchConfiguration("use_agnocast"), "' == '1'"])
        ),
    )
    set_container_package_agnocast = SetLaunchConfiguration(
        "container_package",
        "agnocast_components",
        condition=IfCondition(
            PythonExpression(["'", LaunchConfiguration("use_agnocast"), "' == '1'"])
        ),
    )

    set_container_executable_default = SetLaunchConfiguration(
        "container_executable",
        "component_container",
        condition=UnlessCondition(LaunchConfiguration("use_multithread")),
    )
    set_container_executable_default_mt = SetLaunchConfiguration(
        "container_executable",
        "component_container_mt",
        condition=IfCondition(LaunchConfiguration("use_multithread")),
    )
    set_container_executable_agnocast = SetLaunchConfiguration(
        "container_executable",
        "agnocast_component_container_cie",
        condition=IfCondition(
            PythonExpression(
                [
                    "'",
                    LaunchConfiguration("use_agnocast"),
                    "' == '1' and '",
                    LaunchConfiguration("use_multithread"),
                    "' != 'true' and '",
                    LaunchConfiguration("use_multithread"),
                    "' != 'True'",
                ]
            )
        ),
    )
    set_container_executable_agnocast_mt = SetLaunchConfiguration(
        "container_executable",
        "agnocast_component_container_mt",
        condition=IfCondition(
            PythonExpression(
                [
                    "'",
                    LaunchConfiguration("use_agnocast"),
                    "' == '1' and ('",
                    LaunchConfiguration("use_multithread"),
                    "' == 'true' or '",
                    LaunchConfiguration("use_multithread"),
                    "' == 'True')",
                ]
            )
        ),
    )

    set_ld_preload_value = SetLaunchConfiguration(
        "ld_preload_value",
        PythonExpression(
            ["'libagnocast_heaphook.so:' + '", EnvironmentVariable("LD_PRELOAD", default_value=""), "'"]
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_multithread", default_value="false"),
            use_agnocast,
            set_container_package_default,
            set_container_package_agnocast,
            set_container_executable_default,
            set_container_executable_default_mt,
            set_container_executable_agnocast,
            set_container_executable_agnocast_mt,
            set_ld_preload_value,
        ]
    )
