"""
Object handling for Engli runtime.
"""

from typing import Dict, Optional
from dataclasses import dataclass

from .values import Value, create_object


@dataclass
class EngliObject:
    """An Engli object."""

    name: str
    properties: Dict[str, Value]

    def get_property(self, name: str) -> Optional[Value]:
        """Get a property value."""
        return self.properties.get(name)

    def set_property(self, name: str, value: Value) -> None:
        """Set a property value."""
        self.properties[name] = value
