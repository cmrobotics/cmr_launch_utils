from typing import Text
from launch.launch_context import LaunchContext
from launch import Substitution, Condition


class IfElseSubstitution(Substitution):
    def __init__(self, condition: Condition, if_true: Substitution, if_false: Substitution) -> None:
        """Create a IfElseSubstitution."""
        super().__init__()
        self.__condition = condition
        self.__if_true = if_true
        self.__if_false = if_false

    @property
    def condition(self) -> Substitution:
        return self.__condition

    @property
    def if_true(self) -> Substitution:
        return self.__if_true

    @property
    def if_false(self) -> Substitution:
        return self.__if_false

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return "{} if {} else {}".format(self.if_true.describe(), self.condition.describe(), self.if_false.describe())

    def perform(self, context: LaunchContext) -> Text:
        """Perform the substitution by retrieving the local variable."""
        return self.if_true.perform(context) if self.condition.evaluate(context) is True else self.if_false.perform(context)