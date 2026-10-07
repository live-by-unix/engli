"""
Tests for the Engli parser.
"""

import pytest

from engli.lexer import Lexer
from engli.parser import Parser
from engli.ast import NodeType, VariableDeclaration, Literal, Identifier, BinaryOperation


class TestParser:
    """Test parser functionality."""

    def test_variable_declaration(self):
        """Test parsing variable declarations."""
        lexer = Lexer('Set x to 10.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert stmt.node_type == NodeType.VARIABLE_DECLARATION
        assert stmt.name == "x"
        assert isinstance(stmt.value, Literal)
        assert stmt.value.value == 10

    def test_arithmetic_expression(self):
        """Test parsing arithmetic expressions."""
        lexer = Lexer('Set x to 10 plus 5.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert isinstance(stmt.value, BinaryOperation)
        assert stmt.value.operator == "plus"

    def test_if_statement(self):
        """Test parsing if statements."""
        lexer = Lexer('If x is greater than 10:\n    Say "Hello".\nOtherwise:\n    Say "Goodbye".')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.node_type == NodeType.IF_STATEMENT
        assert stmt.else_block is not None

    def test_while_loop(self):
        """Test parsing while loops."""
        lexer = Lexer('While x is less than 10:\n    Add 1 to x.\nEnd the loop.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.node_type == NodeType.WHILE_LOOP

    def test_for_loop(self):
        """Test parsing for loops."""
        lexer = Lexer('For each item in items:\n    Say item.\nEnd the loop.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.node_type == NodeType.FOR_LOOP

    def test_function_declaration(self):
        """Test parsing function declarations."""
        lexer = Lexer('Define a function called add that takes a and b:\n    Return a plus b.\nEnd the function.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.node_type == NodeType.FUNCTION_DECLARATION
        assert stmt.name == "add"
        assert stmt.parameters == ["a", "b"]

    def test_list_literal(self):
        """Test parsing list literals."""
        lexer = Lexer('Set x to a list containing 1, 2, and 3.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.value.node_type == NodeType.LIST_LITERAL

    def test_map_literal(self):
        """Test parsing map literals."""
        lexer = Lexer('Set x to a map containing: "key" mapped to "value".')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.value.node_type == NodeType.MAP_LITERAL

    def test_say_statement(self):
        """Test parsing say statements."""
        lexer = Lexer('Say "Hello".')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.node_type == NodeType.SAY

    def test_function_call(self):
        """Test parsing function calls."""
        lexer = Lexer('Set result to add with 10 and 20.')
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        stmt = program.statements[0]
        assert stmt.value.node_type == NodeType.CALL
