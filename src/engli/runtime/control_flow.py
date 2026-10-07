"""
Control flow exceptions for Engli runtime.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ReturnValue:
    """A return value from a function."""

    value: Optional["Value"]


@dataclass
class BreakException(Exception):
    """Exception to break out of a loop."""

    pass


@dataclass
class ContinueException(Exception):
    """Exception to continue to the next loop iteration."""

    pass
