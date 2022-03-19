from typing import Text
from launch.launch_context import LaunchContext
from launch import Substitution
from ament_index_python.packages import get_package_share_directory


class PackageShareDirectorySubstitution(Substitution):
    def __init__(self, package_name: Substitution) -> None:
        """Create a IfElseSubstitution."""
        super().__init__()
        self.__package_name = package_name

    @property
    def package_name(self) -> Substitution:
        return self.__package_name

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return "Package \"{}\" share directory".format(self.package_name.describe())

    def perform(self, context: LaunchContext) -> Text:
        """Perform the substitution."""
        return get_package_share_directory(self.package_name.perform(context))
