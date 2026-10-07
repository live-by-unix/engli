"""
Tests for Engli runtime environment.
"""

import pytest

from engli.runtime import Environment, create_number, create_text


class TestEnvironment:
    """Test environment functionality."""

    def test_define_and_get(self):
        """Test defining and getting variables."""
        env = Environment()
        value = create_number(42)
        env.define("x", value)

        retrieved = env.get("x")
        assert retrieved is not None
        assert retrieved.value == 42

    def test_assign(self):
        """Test variable assignment."""
        env = Environment()
        env.define("x", create_number(10))
        env.assign("x", create_number(20))

        retrieved = env.get("x")
        assert retrieved.value == 20

    def test_nested_environment(self):
        """Test nested environments."""
        parent = Environment()
        parent.define("x", create_number(10))

        child = Environment(parent)
        child.define("y", create_number(20))

        assert child.get("x").value == 10
        assert child.get("y").value == 20
        assert parent.get("y") is None

    def test_constant_reassignment(self):
        """Test that constants cannot be reassigned."""
        env = Environment()
        env.define("x", create_number(10), is_constant=True)

        result = env.assign("x", create_number(20))
        assert result is False

    def test_exists(self):
        """Test variable existence check."""
        env = Environment()
        env.define("x", create_number(10))

        assert env.exists("x") is True
        assert env.exists("y") is False
