from typing import List
from .command import Command

class CommandDispatcher:
    def __init__(self):
        self._history: List[Command] = []

    def execute(self, command: Command):
        result = command.execute()
        self._history.append(command)
        return result

    def undo(self):
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        return True

    def get_history(self) -> List[str]:
        return [cmd.description() for cmd in self._history]