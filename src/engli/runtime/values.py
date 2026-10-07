"""
Runtime value system for Engli.
"""

from dataclasses import dataclass
from typing import Any, List, Dict, Set, Callable, Optional
from enum import Enum


class ValueType(Enum):
    """Types of runtime values."""

    NUMBER = "number"
    DECIMAL = "decimal"
    TEXT = "text"
    BOOLEAN = "boolean"
    CHARACTER = "character"
    NOTHING = "nothing"
    LIST = "list"
    MAP = "map"
    SET = "set"
    FUNCTION = "function"
    OBJECT = "object"
    TYPE = "type"
    ENUM = "enum"
    ERROR = "error"


@dataclass
class Value:
    """A runtime value in Engli."""

    type: ValueType
    value: Any

    def __str__(self) -> str:
        if self.type == ValueType.NOTHING:
            return "nothing"
        if self.type == ValueType.TEXT:
            return f'"{self.value}"'
        if self.type == ValueType.BOOLEAN:
            return "true" if self.value else "false"
        return str(self.value)

    def __repr__(self) -> str:
        return f"Value({self.type}, {self.value})"

    def is_truthy(self) -> bool:
        """Check if a value is truthy."""
        if self.type == ValueType.NOTHING:
            return False
        if self.type == ValueType.BOOLEAN:
            return self.value
        if self.type == ValueType.NUMBER or self.type == ValueType.DECIMAL:
            return self.value != 0
        if self.type == ValueType.TEXT:
            return len(self.value) > 0
        if self.type == ValueType.LIST or self.type == ValueType.SET:
            return len(self.value) > 0
        if self.type == ValueType.MAP:
            return len(self.value) > 0
        return True


def create_number(value: int) -> Value:
    """Create a number value."""
    return Value(ValueType.NUMBER, value)


def create_decimal(value: float) -> Value:
    """Create a decimal value."""
    return Value(ValueType.DECIMAL, value)


def create_text(value: str) -> Value:
    """Create a text value."""
    return Value(ValueType.TEXT, value)


def create_boolean(value: bool) -> Value:
    """Create a boolean value."""
    return Value(ValueType.BOOLEAN, value)


def create_nothing() -> Value:
    """Create a nothing value."""
    return Value(ValueType.NOTHING, None)


def create_list(elements: List[Value]) -> Value:
    """Create a list value."""
    return Value(ValueType.LIST, elements)


def create_map(pairs: Dict[str, Value]) -> Value:
    """Create a map value."""
    return Value(ValueType.MAP, pairs)


def create_set(elements: Set[Any]) -> Value:
    """Create a set value."""
    return Value(ValueType.SET, elements)


def create_function(name: str, params: List[str], body: List, closure: Any) -> Value:
    """Create a function value."""
    return Value(ValueType.FUNCTION, {"name": name, "params": params, "body": body, "closure": closure})


def create_object(name: str, properties: Dict[str, Value]) -> Value:
    """Create an object value."""
    return Value(ValueType.OBJECT, {"name": name, "properties": properties})


def create_error(message: str, error_type: str = "RuntimeError") -> Value:
    """Create an error value."""
    return Value(ValueType.ERROR, {"message": message, "type": error_type})
