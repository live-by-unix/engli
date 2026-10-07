"""
Integration tests for Engli example programs.
"""

import pytest
from pathlib import Path

from engli.lexer import Lexer
from engli.parser import Parser
from engli.runtime import Interpreter


class TestExamples:
    """Test example programs."""

    def test_hello_example(self):
        """Test the hello.engli example."""
        source = Path("examples/hello.engli").read_text()

        lexer = Lexer(source, "examples/hello.engli")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        # Program should run without errors
        assert result is None

    def test_variables_example(self):
        """Test the variables.engli example."""
        source = Path("examples/variables.engli").read_text()

        lexer = Lexer(source, "examples/variables.engli")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        assert result is None

    def test_functions_example(self):
        """Test the functions.engli example."""
        source = Path("examples/functions.engli").read_text()

        lexer = Lexer(source, "examples/functions.engli")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        assert result is None

    def test_recursion_example(self):
        """Test the recursion.engli example."""
        source = Path("examples/recursion.engli").read_text()

        lexer = Lexer(source, "examples/recursion.engli")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        assert result is None

    def test_loops_example(self):
        """Test the loops.engli example."""
        source = Path("examples/loops.engli").read_text()

        lexer = Lexer(source, "examples/loops.engli")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        assert result is None

    def test_acceptance_test_sum(self):
        """Test the acceptance test: sum 1-100."""
        source = """
Set total to 0.

For each number from 1 through 100:

    Add number to total.

Say total.
"""

        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        total = interpreter.environment.get("total")
        assert total.value == 5050

    def test_acceptance_test_factorial(self):
        """Test the acceptance test: factorial."""
        source = """
Define a function called factorial that takes n:

    If n is less than or equal to 1:

        Return 1.

    Return n multiplied by factorial with n minus 1.

End the function.

Set result to factorial with 10.
Say result.
"""

        lexer = Lexer(source, "<test>")
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(program)

        # The result variable should be 3628800
        assert result is None
        final_result = interpreter.environment.get("result")
        assert final_result is not None
        assert final_result.value == 3628800
