from __future__ import annotations

"""
Runtime errors for Engli.
"""

from typing import Optional, List

from ..lexer.tokens import SourceLocation


class EngliRuntimeError(Exception):
    """A runtime error in Engli."""

    def __init__(self, message: str, location: SourceLocation, stack_trace: List[str]):
        self.message = message
        self.location = location
        self.stack_trace = stack_trace
        super().__init__(self.__str__())

    def __str__(self) -> str:
        lines = [f"RuntimeError: {self.message}"]
        lines.append(f"  at {self.location}")

        if self.stack_trace:
            lines.append("")
            lines.append("Stack trace:")
            for frame in self.stack_trace:
                lines.append(f"  {frame}")

        return "\n".join(lines)
