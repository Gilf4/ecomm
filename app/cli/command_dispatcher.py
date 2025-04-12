from typing import List
from .command import Command

class CommandDispatcher:
    def __init__(self):
        self._history: List[Command] = []
        self._undo_stack: List[Command] = []

    def execute(self, command: Command):
        result = command.execute()
        self._history.append(command)
        return result

    def undo(self):
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        self._undo_stack.append(command)
        return True

    def redo(self):
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        command.execute()
        self._history.append(command)
        return True

    def get_history(self) -> List[str]:
        return [cmd.description() for cmd in self._history]