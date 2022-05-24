# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is a copy from append_environment_varaible.py from ros/launch
# commit hash 8adf7deccd47eb81d773acf7d2f3c285c1c04bd2. The file was copied
# because this action was not present in Galactic.

"""Module for the AppendEnvironmentVariable action."""

from pathlib import Path
from typing import List

from launch.action import Action
from launch.frontend import Entity
from launch.frontend import expose_action
from launch.frontend import Parser
from launch.launch_context import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch.substitution import Substitution
from launch.utilities import normalize_to_list_of_substitutions
from launch.utilities import perform_substitutions


@expose_action('touch_file')
class TouchFile(Action):
    """
    Action that "touches" (creates) a file and its parent directories
    """

    def __init__(
        self,
        path: SomeSubstitutionsType,
        **kwargs,
    ) -> None:
        """
        Create an AppendEnvironmentVariable action.

        All parameters can be provided as substitutions.
        A substitution for the prepend parameter will be coerced to `bool` following YAML rules.

        :param path: the name of the environment variable
        """
        super().__init__(**kwargs)
        self.__path = normalize_to_list_of_substitutions(path)

    @classmethod
    def parse(
        cls,
        entity: Entity,
        parser: Parser,
    ):
        """Parse a 'touch_file' entity."""
        _, kwargs = super().parse(entity, parser)
        kwargs['path'] = parser.parse_substitution(entity.get_attr('path'))
        return cls, kwargs

    @property
    def path(self) -> List[Substitution]:
        """Getter for the path to the file that will be created."""
        return self.__path

    def execute(self, context: LaunchContext) -> None:
        """Execute the action."""
        path = Path(perform_substitutions(context, self.path))
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        # Touch the file
        path.touch()
        return None
