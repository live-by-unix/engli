"""
Tests for the Engli interpreter.
"""

import pytest

from engli.lexer import Lexer
from engli.parser import Parser
from engli.runtime import Interpreter, create_number, create_text


class TestInterpreter:
    """Test interpreter functionality."""

    def test_variable_declaration(self):
        """Test variable declaration."""
        lexer = Lexer('Set x to 10.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        value = interpreter.environment.get("x")
        assert value is not None
        assert value.value == 10

    def test_arithmetic(self):
        """Test arithmetic operations."""
        lexer = Lexer('Set x to 10 plus 5.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        value = interpreter.environment.get("x")
        assert value.value == 15

    def test_string_concatenation(self):
        """Test string concatenation."""
        lexer = Lexer('Set x to "Hello" plus " World".')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        value = interpreter.environment.get("x")
        assert value.value == "Hello World"

    def test_comparisons(self):
        """Test comparison operations."""
        lexer = Lexer('Set x to 10 is greater than 5.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        value = interpreter.environment.get("x")
        assert value.value is True

    def test_boolean_logic(self):
        """Test boolean logic."""
        lexer = Lexer('Set x to true and false.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        value = interpreter.environment.get("x")
        assert value.value is False

    def test_if_statement(self):
        """Test if statement execution."""
        lexer = Lexer('Set x to 10.\nIf x is greater than 5:\n    Set y to 20.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        y = interpreter.environment.get("y")
        assert y is not None
        assert y.value == 20

    def test_while_loop(self):
        """Test while loop execution."""
        lexer = Lexer('Set x to 0.\nWhile x is less than 5:\n    Add 1 to x.\nEnd the loop.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        x = interpreter.environment.get("x")
        assert x.value == 5

    def test_function_call(self):
        """Test function call execution."""
        lexer = Lexer('Define a function called add that takes x and y:\n    Return x plus y.\nEnd the function.\nSet result to add with 10 and 20.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        result = interpreter.environment.get("result")
        assert result.value == 30

    def test_recursion(self):
        """Test recursive function execution."""
        lexer = Lexer('Define a function called factorial that takes n:\n    If n is less than 2:\n        Return 1.\n    Return n multiplied by factorial with n minus 1.\nEnd the function.\nSet result to factorial with 5.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        result = interpreter.environment.get("result")
        assert result.value == 120

        result = interpreter.environment.get("result")
        assert result.value == 120

    def test_list_operations(self):
        """Test list operations."""
        lexer = Lexer('Set numbers to a list containing 1, 2, and 3.\nAdd 4 to numbers.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        numbers = interpreter.environment.get("numbers")
        assert len(numbers.value) == 4

    def test_map_operations(self):
        """Test map operations."""
        lexer = Lexer('Set person to a map containing: "name" mapped to "AB".')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

        person = interpreter.environment.get("person")
        assert "name" in person.value
        assert person.value["name"].value == "AB"
