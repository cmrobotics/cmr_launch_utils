from typing import Text, Iterable
from launch.launch_context import LaunchContext
from launch.some_substitutions_type import SomeSubstitutionsType
from launch import Substitution


class TextFormatSubstitution(Substitution):
    def __init__(self, fmt: Text, substitutions: Iterable[SomeSubstitutionsType]) -> None:
        """Create a TextFormatSubstitution."""
        from launch.utilities import normalize_to_list_of_substitutions
        self.__substitutions = normalize_to_list_of_substitutions(substitutions)
        self.__format = fmt

    @property
    def substitutions(self) -> Iterable[Substitution]:
        """Getter for variable_name."""
        return self.__substitutions

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return "LocalVar('{}')".format(' + '.join([s.describe() for s in self.substitutions]))

    def perform(self, context: LaunchContext) -> Text:
        """Perform the substitution by retrieving the local variable."""
        performed_substitutions = [sub.perform(context) for sub in self.__substitutions]
        return self.__format.format(*performed_substitutions)
