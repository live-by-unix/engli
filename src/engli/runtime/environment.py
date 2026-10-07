"""
Environment for managing variable scopes in Engli.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass

from .values import Value


@dataclass
class Environment:
    """A lexical environment for variable storage."""

    parent: Optional["Environment"]
    values: Dict[str, Value]
    constants: set

    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.values = {}
        self.constants = set()

    def define(self, name: str, value: Value, is_constant: bool = False) -> None:
        """Define a variable in the current environment."""
        if is_constant:
            self.constants.add(name)
        self.values[name] = value

    def assign(self, name: str, value: Value) -> bool:
        """Assign a value to a variable."""
        if name in self.constants:
            return False

        if name in self.values:
            self.values[name] = value
            return True

        if self.parent:
            return self.parent.assign(name, value)

        return False

    def get(self, name: str) -> Optional[Value]:
        """Get a variable's value."""
        if name in self.values:
            return self.values[name]

        if self.parent:
            return self.parent.get(name)

        return None

    def exists(self, name: str) -> bool:
        """Check if a variable exists."""
        if name in self.values:
            return True

        if self.parent:
            return self.parent.exists(name)

        return False
