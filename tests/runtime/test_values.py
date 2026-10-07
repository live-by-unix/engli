"""
Tests for Engli runtime values.
"""

import pytest

from engli.runtime import Value, ValueType, create_number, create_text, create_boolean, create_nothing, create_list, create_map


class TestValues:
    """Test runtime value functionality."""

    def test_number_value(self):
        """Test number value creation."""
        value = create_number(42)
        assert value.type == ValueType.NUMBER
        assert value.value == 42

    def test_text_value(self):
        """Test text value creation."""
        value = create_text("hello")
        assert value.type == ValueType.TEXT
        assert value.value == "hello"

    def test_boolean_value(self):
        """Test boolean value creation."""
        value = create_boolean(True)
        assert value.type == ValueType.BOOLEAN
        assert value.value is True

    def test_nothing_value(self):
        """Test nothing value creation."""
        value = create_nothing()
        assert value.type == ValueType.NOTHING
        assert value.value is None

    def test_list_value(self):
        """Test list value creation."""
        value = create_list([create_number(1), create_number(2)])
        assert value.type == ValueType.LIST
        assert len(value.value) == 2

    def test_map_value(self):
        """Test map value creation."""
        value = create_map({"key": create_text("value")})
        assert value.type == ValueType.MAP
        assert "key" in value.value

    def test_truthy_number(self):
        """Test truthiness of numbers."""
        assert create_number(1).is_truthy() is True
        assert create_number(0).is_truthy() is False

    def test_truthy_boolean(self):
        """Test truthiness of booleans."""
        assert create_boolean(True).is_truthy() is True
        assert create_boolean(False).is_truthy() is False

    def test_truthy_text(self):
        """Test truthiness of text."""
        assert create_text("hello").is_truthy() is True
        assert create_text("").is_truthy() is False

    def test_truthy_nothing(self):
        """Test truthiness of nothing."""
        assert create_nothing().is_truthy() is False

    def test_truthy_list(self):
        """Test truthiness of lists."""
        assert create_list([create_number(1)]).is_truthy() is True
        assert create_list([]).is_truthy() is False

    def test_value_string_representation(self):
        """Test string representation of values."""
        assert str(create_number(42)) == "42"
        assert str(create_text("hello")) == '"hello"'
        assert str(create_boolean(True)) == "true"
        assert str(create_nothing()) == "nothing"
