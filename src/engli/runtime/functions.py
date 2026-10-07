from __future__ import annotations

"""
Function handling for Engli runtime.
"""

from typing import List, Optional, Callable, Any, TYPE_CHECKING
from dataclasses import dataclass

from .values import Value, create_function, ValueType
from .environment import Environment

if TYPE_CHECKING:
    from .interpreter import Interpreter


@dataclass
class EngliFunction:
    """An Engli function."""

    name: str
    parameters: List[str]
    body: List  # List of AST nodes
    closure: Environment
    interpreter: "Interpreter"

    def call(self, arguments: List[Value]) -> Value:
        """Call the function with arguments."""
        # Create a new environment with the closure as parent
        env = Environment(self.closure)

        # Bind parameters to arguments
        for i, param in enumerate(self.parameters):
            if i < len(arguments):
                env.define(param, arguments[i])
            else:
                env.define(param, Value(ValueType.NOTHING, None))

        # Execute the function body
        result = self.interpreter.execute_block(self.body, env)

        return result if result is not None else Value(ValueType.NOTHING, None)


@dataclass
class BuiltinFunction:
    """A built-in function."""

    name: str
    handler: Callable[[List[Value]], Value]

    def call(self, arguments: List[Value]) -> Value:
        """Call the built-in function."""
        return self.handler(arguments)


def create_builtin_function(name: str, handler: Callable[[List[Value]], Value]) -> Value:
    """Create a built-in function value."""
    return Value(ValueType.FUNCTION, BuiltinFunction(name, handler))
