from __future__ import annotations

"""
Parser for the Engli programming language.
"""

from typing import List, Optional, Union, Any
from dataclasses import dataclass

from ..lexer import Lexer, Token, TokenType, SourceLocation, LexerError
from ..ast import (
    ASTNode,
    NodeType,
    Program,
    VariableDeclaration,
    VariableAssignment,
    ArithmeticAssignment,
    ConstantDeclaration,
    FunctionDeclaration,
    TypeDeclaration,
    EnumDeclaration,
    Export,
    Import,
    IfStatement,
    WhileLoop,
    ForLoop,
    ForRangeLoop,
    RepeatLoop,
    ForeverLoop,
    Break,
    Continue,
    MatchStatement,
    TryStatement,
    Say,
    Ask,
    TaskStart,
    TaskWait,
    ChannelCreate,
    ChannelSend,
    ChannelReceive,
    Literal,
    Identifier,
    BinaryOperation,
    UnaryOperation,
    Call,
    PropertyAccess,
    IndexAccess,
    ListLiteral,
    MapLiteral,
    SetLiteral,
    ObjectLiteral,
    TypeConstruction,
    EnumMember,
    Optional as OptionalNode,
    StringInterpolation,
    Return,
    PropertyAssignment,
    IndexAssignment,
    ListAdd,
    ListRemove,
    ListRemove,
    FileRead,
    FileWrite,
    FileAppend,
    FileExists,
    DirectoryCreate,
    DirectoryList,
    FileDelete,
    EnvGet,
    EnvSet,
    CommandRun,
    ShellRun,
    HttpRequest,
    JsonParse,
    JsonStringify,
    TimeNow,
    TimeTimestamp,
    TimeSleep,
    RandomNumber,
)


@dataclass
class ParseError:
    """An error from the parser."""

    message: str
    location: SourceLocation


class Parser:
    """Parses Engli tokens into an AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors: List[ParseError] = []

    def current_token(self) -> Optional[Token]:
        """Get the current token."""
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a token."""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def advance(self) -> Optional[Token]:
        """Advance to the next token."""
        token = self.current_token()
        if token is not None:
            self.position += 1
        return token

    def consume(self, token_type: TokenType, value: Optional[str] = None) -> Optional[Token]:
        """Consume a token of the expected type."""
        token = self.current_token()
        if token is None:
            self.error(f"Expected {token_type.name}, got EOF")
            return None

        if token.type != token_type:
            if value is not None:
                self.error(f"Expected {value}, got {token.value}")
            else:
                self.error(f"Expected {token_type.name}, got {token.type.name}")
            return None

        if value is not None and token.value.lower() != value.lower():
            self.error(f"Expected {value}, got {token.value}")
            return None

        return self.advance()

    def check(self, token_type: TokenType, value: Optional[str] = None) -> bool:
        """Check if the current token matches."""
        token = self.current_token()
        if token is None:
            return False

        if token.type != token_type:
            return False

        if value is not None and token.value.lower() != value.lower():
            return False

        return True

    def match_keyword(self, *keywords: str) -> bool:
        """Check if the current token is any of the given keywords."""
        token = self.current_token()
        if token is None or token.type != TokenType.KEYWORD:
            return False
        return token.value.lower() in [k.lower() for k in keywords]

    def error(self, message: str) -> None:
        """Report a parse error."""
        token = self.current_token()
        location = token.location if token else SourceLocation("<unknown>", 0, 0, "")
        self.errors.append(ParseError(message, location))

    def skip_newlines(self) -> None:
        """Skip newline tokens."""
        while self.check(TokenType.NEWLINE):
            self.advance()

    def parse(self) -> Program:
        """Parse the entire token stream into a program."""
        statements: List[ASTNode] = []
        max_iterations = 10000  # Safety limit
        iterations = 0

        while self.current_token() and self.current_token().type != TokenType.EOF:
            iterations += 1
            if iterations > max_iterations:
                self.error("Parser exceeded maximum iterations - possible infinite loop")
                break

            self.skip_newlines()
            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                else:
                    # If we can't parse a statement, advance to avoid infinite loop
                    self.advance()

        location = SourceLocation("<program>", 1, 1, "")
        return Program(NodeType.PROGRAM, location, statements)

    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a statement."""
        self.skip_newlines()

        token = self.current_token()
        if token is None:
            return None

        # Arithmetic assignment: Add 5 to x (check before "set" to avoid conflict)
        if self.check(TokenType.KEYWORD, "add") or self.check(TokenType.IDENTIFIER, "add"):
            return self.parse_arithmetic_assignment()
        if self.check(TokenType.KEYWORD, "subtract"):
            return self.parse_arithmetic_assignment()
        if self.check(TokenType.KEYWORD, "multiplied"):
            return self.parse_arithmetic_assignment()
        if self.check(TokenType.KEYWORD, "divided"):
            return self.parse_arithmetic_assignment()
        if self.check(TokenType.KEYWORD, "modulo"):
            return self.parse_arithmetic_assignment()

        # List operations (e.g., "Remove 3 from numbers")
        if self.check(TokenType.KEYWORD, "remove"):
            return self.parse_list_remove()

        # Variable declaration: Set x to 10
        if self.match_keyword("set"):
            return self.parse_variable_declaration()

        # Function/Type/Enum/Constant declarations: Define ...
        if self.check(TokenType.KEYWORD, "define"):
            self.consume(TokenType.KEYWORD, "define")
            if self.peek_token() and self.peek_token().value.lower() == "a":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "function":
                    return self.parse_function_declaration()
                return self.parse_type_declaration()
            if self.peek_token() and self.peek_token().value.lower() == "an":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "enumeration":
                    return self.parse_enum_declaration()
                return self.parse_type_declaration()
            if self.peek_token() and self.peek_token().value.lower() == "function":
                return self.parse_function_declaration()
            if self.peek_token() and self.peek_token().value.lower() == "the":
                return self.parse_constant_declaration()
            if self.peek_token() and self.peek_token().value.lower() == "enumeration":
                return self.parse_enum_declaration()
            # Otherwise, it's a constant declaration
            return self.parse_constant_declaration()

        # If statement
        if self.match_keyword("if"):
            return self.parse_if_statement()

        # While loop
        if self.match_keyword("while"):
            return self.parse_while_loop()

        # For loop
        if self.match_keyword("for"):
            return self.parse_for_loop()

        # Repeat loop
        if self.match_keyword("repeat"):
            return self.parse_repeat_loop()

        # Forever loop
        if self.match_keyword("forever"):
            return self.parse_forever_loop()

        # Break
        if self.match_keyword("break"):
            return self.parse_break()

        # Continue
        if self.match_keyword("continue"):
            return self.parse_continue()

        # Match statement
        if self.match_keyword("match"):
            return self.parse_match_statement()

        # Try statement
        if self.match_keyword("try"):
            return self.parse_try_statement()

        # Say
        if self.match_keyword("say"):
            return self.parse_say()

        # Ask
        if self.match_keyword("ask"):
            return self.parse_ask()

        # Return
        if self.match_keyword("return"):
            return self.parse_return()

        # Export
        if self.match_keyword("export"):
            return self.parse_export()

        # Import
        if self.match_keyword("import"):
            return self.parse_import()

        # Task start
        if self.match_keyword("start"):
            return self.parse_task_start()

        # Task wait
        if self.match_keyword("wait"):
            return self.parse_task_wait()

        # Channel create
        if self.match_keyword("create"):
            if self.peek_token() and self.peek_token().value.lower() == "a":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "channel":
                    return self.parse_channel_create()

        # Channel send
        if self.match_keyword("send"):
            return self.parse_channel_send()

        # Channel receive
        if self.match_keyword("receive"):
            return self.parse_channel_receive()

        # File operations
        if self.match_keyword("read"):
            return self.parse_file_read()

        if self.match_keyword("write"):
            return self.parse_file_write()

        if self.match_keyword("append"):
            return self.parse_file_append()

        if self.match_keyword("create"):
            if self.peek_token() and self.peek_token().value.lower() == "the":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "directory":
                    return self.parse_directory_create()

        if self.match_keyword("list"):
            return self.parse_directory_list()

        if self.match_keyword("delete"):
            return self.parse_file_delete()

        # Environment
        if self.match_keyword("get"):
            if self.peek_token() and self.peek_token().value.lower() == "the":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "environment":
                    return self.parse_env_get()

        if self.match_keyword("set"):
            if self.peek_token() and self.peek_token().value.lower() == "the":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "environment":
                    return self.parse_env_set()

        # Process
        if self.match_keyword("run"):
            if self.peek_token() and self.peek_token().value.lower() == "the":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "command":
                    return self.parse_command_run()
            if self.peek_token() and self.peek_token().value.lower() == "the":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "shell":
                    return self.parse_shell_run()

        # HTTP
        if self.match_keyword("send"):
            if self.peek_token() and self.peek_token().value.lower() == "a":
                return self.parse_http_request()

        # JSON
        if self.match_keyword("parse"):
            return self.parse_json_parse()

        if self.match_keyword("convert"):
            return self.parse_json_stringify()

        # Time
        if self.match_keyword("set"):
            if self.peek_token() and self.peek_token().value.lower() == "to":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "the":
                    if self.peek_token(3) and self.peek_token(3).value.lower() == "current":
                        if self.peek_token(4) and self.peek_token(4).value.lower() == "date":
                            return self.parse_time_now()
                        if self.peek_token(4) and self.peek_token(4).value.lower() == "unix":
                            return self.parse_time_timestamp()

        if self.match_keyword("wait"):
            if self.peek_token() and self.peek_token().value.lower() == "for":
                return self.parse_time_sleep()

        # Random
        if self.match_keyword("set"):
            if self.peek_token() and self.peek_token().value.lower() == "to":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "a":
                    if self.peek_token(3) and self.peek_token(3).value.lower() == "random":
                        return self.parse_random_number()

        # Object creation
        if self.match_keyword("create"):
            if self.peek_token() and self.peek_token().value.lower() == "an":
                if self.peek_token(2) and self.peek_token(2).value.lower() == "object":
                    return self.parse_object_literal()

        # Expression as statement (e.g., function call)
        expr = self.parse_expression()
        if expr:
            # Check if it's a call
            if isinstance(expr, Call):
                return expr
            # Check if it's an assignment
            if self.check(TokenType.KEYWORD, "to"):
                return self.parse_variable_assignment_from_expr(expr)

        self.error(f"Unexpected token: {token.value}")
        return None

    def parse_variable_declaration(self) -> Optional[VariableDeclaration]:
        """Parse: Set x to 10."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "set")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.KEYWORD, "to")

        # Check if this is a complex value (list, map, set, type construction)
        # that might use "and" as a separator, not a binary operator
        if self.check(TokenType.KEYWORD, "a"):
            value = self.parse_primary()
        else:
            value = self.parse_expression()

        if not value:
            return None

        # Only consume period if the value parser didn't already consume it
        # (e.g., function calls consume their own period)
        if self.check(TokenType.PERIOD):
            self.consume(TokenType.PERIOD)

        return VariableDeclaration(NodeType.VARIABLE_DECLARATION, location, name_token.value, value)

    def parse_arithmetic_assignment(self) -> Optional[ArithmeticAssignment]:
        """Parse: Add 5 to x, Subtract 5 from x, Multiply x by 2, Divide x by 2."""
        location = self.current_token().location

        # Determine and consume the operator
        if self.check(TokenType.KEYWORD, "add") or self.check(TokenType.IDENTIFIER, "add"):
            operator = "add"
            self.advance()
        elif self.check(TokenType.KEYWORD, "subtract"):
            operator = "subtract"
            self.consume(TokenType.KEYWORD, "subtract")
        elif self.check(TokenType.KEYWORD, "multiplied"):
            operator = "multiply"
            self.consume(TokenType.KEYWORD, "multiplied")
        elif self.check(TokenType.KEYWORD, "divided"):
            operator = "divide"
            self.consume(TokenType.KEYWORD, "divided")
        elif self.check(TokenType.KEYWORD, "modulo"):
            operator = "modulo"
            self.consume(TokenType.KEYWORD, "modulo")
        else:
            self.error("Expected arithmetic operator")
            return None

        # Parse the value (for add/subtract) or target (for multiply/divide)
        # For "add/subtract": parse value then "to/from" then target
        # For "multiply/divide": parse target then "by" then value
        if operator in ("add", "subtract"):
            value = self.parse_expression()
            if not value:
                return None

            # Check for preposition
            if operator == "add":
                if not self.check(TokenType.KEYWORD, "to"):
                    self.error("Expected 'to' in arithmetic assignment")
                    return None
                self.consume(TokenType.KEYWORD, "to")
            else:  # subtract
                if not self.check(TokenType.KEYWORD, "from"):
                    self.error("Expected 'from' in arithmetic assignment")
                    return None
                self.consume(TokenType.KEYWORD, "from")

            name_token = self.consume(TokenType.IDENTIFIER)
        else:  # multiply, divide, modulo
            name_token = self.consume(TokenType.IDENTIFIER)
            if not name_token:
                return None

            # Check for "by" keyword
            if not self.check(TokenType.KEYWORD, "by"):
                self.error("Expected 'by' in arithmetic assignment")
                return None
            self.consume(TokenType.KEYWORD, "by")

            value = self.parse_expression()
            if not value:
                return None

        self.consume(TokenType.PERIOD)

        return ArithmeticAssignment(NodeType.ARITHMETIC_ASSIGNMENT, location, operator, name_token.value, value)

    def parse_list_add(self) -> Optional[ASTNode]:
        """Parse: Add 6 to numbers (list append)."""
        location = self.current_token().location
        # Consume "add" (could be KEYWORD or IDENTIFIER)
        self.advance()

        # Parse the value to add
        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "to")

        # Parse the target list
        target = self.parse_primary()
        if not target:
            return None

        self.consume(TokenType.PERIOD)

        return ListAdd(NodeType.LIST_ADD, location, target, value)

    def parse_list_remove(self) -> Optional[ASTNode]:
        """Parse: Remove 3 from numbers."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "remove")

        # Parse the value to remove
        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "from")

        # Parse the target list
        target = self.parse_primary()
        if not target:
            return None

        self.consume(TokenType.PERIOD)

        return ListRemove(NodeType.LIST_REMOVE, location, target, value)

    def parse_variable_assignment_from_expr(self, target: ASTNode) -> Optional[ASTNode]:
        """Parse assignment when we already have the target expression."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "to")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.PERIOD)

        # Check if it's a property assignment
        if isinstance(target, PropertyAccess):
            return PropertyAssignment(NodeType.PROPERTY_ASSIGNMENT, location, target.object, target.property, value)

        # Check if it's an index assignment
        if isinstance(target, IndexAccess):
            return IndexAssignment(NodeType.INDEX_ASSIGNMENT, location, target.object, target.index, value)

        # Regular variable assignment
        if isinstance(target, Identifier):
            return VariableAssignment(NodeType.VARIABLE_ASSIGNMENT, location, target.name, value)

        self.error("Invalid assignment target")
        return None

    def parse_constant_declaration(self) -> Optional[ConstantDeclaration]:
        """Parse: Define the constant MAX as 100."""
        location = self.current_token().location
        # "define" already consumed by match_keyword
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "constant")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.KEYWORD, "as")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.PERIOD)

        return ConstantDeclaration(NodeType.CONSTANT_DECLARATION, location, name_token.value, value)

    def parse_function_declaration(self) -> Optional[FunctionDeclaration]:
        """Parse: Define a function called add that takes a and b: ... End the function."""
        location = self.current_token().location
        # "define" already consumed by match_keyword
        self.consume(TokenType.KEYWORD, "a")
        self.consume(TokenType.KEYWORD, "function")
        self.consume(TokenType.KEYWORD, "called")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        # "that" is optional - check if it's a keyword or identifier
        if self.check(TokenType.KEYWORD, "that") or self.check(TokenType.IDENTIFIER, "that"):
            self.advance()

        self.consume(TokenType.KEYWORD, "takes")

        parameters: List[str] = []
        while True:
            # Parameters can be identifiers or keywords (like "a", "an", "b")
            param_token = self.current_token()
            if param_token and (param_token.type == TokenType.IDENTIFIER or param_token.type == TokenType.KEYWORD):
                self.advance()
                parameters.append(param_token.value)
            else:
                break

            if self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")
            else:
                break

        self.consume(TokenType.COLON)

        body = self.parse_block()

        self.consume(TokenType.KEYWORD, "end")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "function")
        self.consume(TokenType.PERIOD)

        return FunctionDeclaration(NodeType.FUNCTION_DECLARATION, location, name_token.value, parameters, body)

    def parse_type_declaration(self) -> Optional[TypeDeclaration]:
        """Parse: Define a type called Player: ..."""
        location = self.current_token().location
        # "define" already consumed by match_keyword
        self.consume(TokenType.KEYWORD, "a")  # or "an"
        self.consume(TokenType.KEYWORD, "type")
        self.consume(TokenType.KEYWORD, "called")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.COLON)

        fields: List[tuple] = []
        while not self.match_keyword("end"):
            self.consume(TokenType.KEYWORD, "a")
            self.consume(TokenType.KEYWORD, name_token.value)
            self.consume(TokenType.KEYWORD, "has")
            self.consume(TokenType.KEYWORD, "a")

            field_name = self.consume(TokenType.IDENTIFIER)
            if not field_name:
                break

            self.consume(TokenType.KEYWORD, "which")
            self.consume(TokenType.KEYWORD, "is")

            type_name = self.consume(TokenType.IDENTIFIER)
            if not type_name:
                break

            fields.append((field_name.value, type_name.value))
            self.consume(TokenType.PERIOD)

        self.consume(TokenType.KEYWORD, "end")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "type")
        self.consume(TokenType.PERIOD)

        return TypeDeclaration(NodeType.TYPE_DECLARATION, location, name_token.value, fields)

    def parse_enum_declaration(self) -> Optional[EnumDeclaration]:
        """Parse: Define an enumeration called Direction containing: ..."""
        location = self.current_token().location
        # "define" already consumed by match_keyword
        self.consume(TokenType.KEYWORD, "an")
        self.consume(TokenType.KEYWORD, "enumeration")
        self.consume(TokenType.KEYWORD, "called")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.KEYWORD, "containing")
        self.consume(TokenType.COLON)

        members: List[str] = []
        while not self.match_keyword("end"):
            member_token = self.consume(TokenType.IDENTIFIER)
            if not member_token:
                break

            members.append(member_token.value)

            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
            elif self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")

        self.consume(TokenType.KEYWORD, "end")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "enumeration")
        self.consume(TokenType.PERIOD)

        return EnumDeclaration(NodeType.ENUM_DECLARATION, location, name_token.value, members)

    def parse_export(self) -> Optional[Export]:
        """Parse: Export function_name."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "export")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.PERIOD)

        return Export(NodeType.EXPORT, location, name_token.value)

    def parse_import(self) -> Optional[Import]:
        """Parse: Import square from the file "./math.engli"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "import")

        # Check if it's a named import or module import
        if self.peek_token() and self.peek_token().value.lower() == "from":
            # Named import: Import square from the file "./math.engli"
            name_token = self.consume(TokenType.IDENTIFIER)
            if not name_token:
                return None

            self.consume(TokenType.KEYWORD, "from")
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "file")

            path_token = self.consume(TokenType.STRING)
            if not path_token:
                return None

            self.consume(TokenType.PERIOD)

            return Import(NodeType.IMPORT, location, path_token.value, name_token.value)
        else:
            # Module import: Import the file "./math.engli"
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "file")

            path_token = self.consume(TokenType.STRING)
            if not path_token:
                return None

            self.consume(TokenType.PERIOD)

            return Import(NodeType.IMPORT, location, path_token.value, None)

    def parse_if_statement(self) -> Optional[IfStatement]:
        """Parse: If condition: ... Otherwise if: ... Otherwise: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "if")

        condition = self.parse_expression()
        if not condition:
            return None

        self.consume(TokenType.COLON)

        then_block = self.parse_block()

        elif_blocks: List[tuple] = []
        while self.match_keyword("otherwise") and self.peek_token() and self.peek_token().value.lower() == "if":
            self.consume(TokenType.KEYWORD, "otherwise")
            self.consume(TokenType.KEYWORD, "if")

            elif_condition = self.parse_expression()
            if not elif_condition:
                break

            self.consume(TokenType.COLON)
            elif_block = self.parse_block()
            elif_blocks.append((elif_condition, elif_block))

        else_block = None
        if self.match_keyword("otherwise"):
            self.consume(TokenType.KEYWORD, "otherwise")
            self.consume(TokenType.COLON)
            else_block = self.parse_block()

        return IfStatement(NodeType.IF_STATEMENT, location, condition, then_block, elif_blocks, else_block)

    def parse_while_loop(self) -> Optional[WhileLoop]:
        """Parse: While condition: ... End the loop."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "while")

        condition = self.parse_expression()
        if not condition:
            return None

        self.consume(TokenType.COLON)

        body = self.parse_block()

        # Optional "End the loop."
        if self.match_keyword("end"):
            self.consume(TokenType.KEYWORD, "end")
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "loop")
            self.consume(TokenType.PERIOD)

        return WhileLoop(NodeType.WHILE_LOOP, location, condition, body)

    def parse_for_loop(self) -> Optional[Union[ForLoop, ForRangeLoop]]:
        """Parse: For each item in items: ... or For each number from 1 through 10: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "for")
        self.consume(TokenType.KEYWORD, "each")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        # Check if it's a range loop (check current token, not peek)
        if self.check(TokenType.KEYWORD, "from"):
            self.consume(TokenType.KEYWORD, "from")

            start = self.parse_expression()
            if not start:
                return None

            self.consume(TokenType.KEYWORD, "through")

            end = self.parse_expression()
            if not end:
                return None

            self.consume(TokenType.COLON)

            body = self.parse_block()

            # Optional "End the loop."
            if self.match_keyword("end"):
                self.consume(TokenType.KEYWORD, "end")
                self.consume(TokenType.KEYWORD, "the")
                self.consume(TokenType.KEYWORD, "loop")
                self.consume(TokenType.PERIOD)

            return ForRangeLoop(NodeType.FOR_RANGE_LOOP, location, variable_token.value, start, end, body)

        # Regular for loop - consume "in"
        self.consume(TokenType.KEYWORD, "in")

        iterable = self.parse_expression()
        if not iterable:
            return None

        self.consume(TokenType.COLON)

        body = self.parse_block()

        # Optional "End the loop."
        if self.match_keyword("end"):
            self.consume(TokenType.KEYWORD, "end")
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "loop")
            self.consume(TokenType.PERIOD)

        return ForLoop(NodeType.FOR_LOOP, location, variable_token.value, iterable, body)

    def parse_repeat_loop(self) -> Optional[RepeatLoop]:
        """Parse: Repeat 10 times: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "repeat")

        count = self.parse_expression()
        if not count:
            return None

        self.consume(TokenType.KEYWORD, "times")
        self.consume(TokenType.COLON)

        body = self.parse_block()

        # Optional "End the repetition."
        if self.match_keyword("end"):
            self.consume(TokenType.KEYWORD, "end")
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "repetition")
            self.consume(TokenType.PERIOD)

        return RepeatLoop(NodeType.REPEAT_LOOP, location, count, body)

    def parse_forever_loop(self) -> Optional[ForeverLoop]:
        """Parse: Forever: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "forever")
        self.consume(TokenType.COLON)

        body = self.parse_block()

        # Optional "End the loop."
        if self.match_keyword("end"):
            self.consume(TokenType.KEYWORD, "end")
            self.consume(TokenType.KEYWORD, "the")
            self.consume(TokenType.KEYWORD, "loop")
            self.consume(TokenType.PERIOD)

        return ForeverLoop(NodeType.FOREVER_LOOP, location, body)

    def parse_break(self) -> Optional[Break]:
        """Parse: Break out of the loop."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "break")
        self.consume(TokenType.KEYWORD, "out")
        self.consume(TokenType.KEYWORD, "of")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "loop")
        self.consume(TokenType.PERIOD)

        return Break(NodeType.BREAK, location)

    def parse_continue(self) -> Optional[Continue]:
        """Parse: Continue with the next iteration."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "continue")
        self.consume(TokenType.KEYWORD, "with")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "next")
        self.consume(TokenType.KEYWORD, "iteration")
        self.consume(TokenType.PERIOD)

        return Continue(NodeType.CONTINUE, location)

    def parse_match_statement(self) -> Optional[MatchStatement]:
        """Parse: Match value: When condition: ... Otherwise: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "match")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.COLON)

        cases: List[tuple] = []
        while self.match_keyword("when"):
            self.consume(TokenType.KEYWORD, "when")

            condition = self.parse_expression()
            if not condition:
                break

            self.consume(TokenType.COLON)
            case_body = self.parse_block()
            cases.append((condition, case_body))

        default_case = None
        if self.match_keyword("otherwise"):
            self.consume(TokenType.KEYWORD, "otherwise")
            self.consume(TokenType.COLON)
            default_case = self.parse_block()

        self.consume(TokenType.KEYWORD, "end")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "match")
        self.consume(TokenType.PERIOD)

        return MatchStatement(NodeType.MATCH_STATEMENT, location, value, cases, default_case)

    def parse_try_statement(self) -> Optional[TryStatement]:
        """Parse: Try: ... If an error occurs as error: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "try")
        self.consume(TokenType.COLON)

        try_block = self.parse_block()

        self.consume(TokenType.KEYWORD, "if")
        self.consume(TokenType.KEYWORD, "an")
        self.consume(TokenType.KEYWORD, "error")
        self.consume(TokenType.KEYWORD, "occurs")
        self.consume(TokenType.KEYWORD, "as")

        error_name_token = self.consume(TokenType.IDENTIFIER)
        if not error_name_token:
            return None

        self.consume(TokenType.COLON)

        catch_block = self.parse_block()

        return TryStatement(NodeType.TRY_STATEMENT, location, try_block, error_name_token.value, catch_block)

    def parse_say(self) -> Optional[Say]:
        """Parse: Say "Hello"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "say")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.PERIOD)

        return Say(NodeType.SAY, location, value)

    def parse_ask(self) -> Optional[Ask]:
        """Parse: Ask the user for their name and store the answer in name."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "ask")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "user")
        self.consume(TokenType.KEYWORD, "for")
        self.consume(TokenType.KEYWORD, "their")

        prompt = self.parse_expression()
        if not prompt:
            return None

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "answer")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return Ask(NodeType.ASK, location, prompt, variable_token.value)

    def parse_return(self) -> Optional[Return]:
        """Parse: Return x."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "return")

        value = None
        if not self.check(TokenType.PERIOD):
            value = self.parse_expression()

        self.consume(TokenType.PERIOD)

        return Return(NodeType.RETURN, location, value)

    def parse_task_start(self) -> Optional[TaskStart]:
        """Parse: Start a task: ..."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "start")
        self.consume(TokenType.KEYWORD, "a")
        self.consume(TokenType.KEYWORD, "task")
        self.consume(TokenType.COLON)

        body = self.parse_block()

        return TaskStart(NodeType.TASK_START, location, body)

    def parse_task_wait(self) -> Optional[TaskWait]:
        """Parse: Wait for task to finish."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "wait")
        self.consume(TokenType.KEYWORD, "for")

        task = self.parse_expression()
        if not task:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "finish")
        self.consume(TokenType.PERIOD)

        return TaskWait(NodeType.TASK_WAIT, location, task)

    def parse_channel_create(self) -> Optional[ChannelCreate]:
        """Parse: Create a channel called messages."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "create")
        self.consume(TokenType.KEYWORD, "a")
        self.consume(TokenType.KEYWORD, "channel")
        self.consume(TokenType.KEYWORD, "called")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.PERIOD)

        return ChannelCreate(NodeType.CHANNEL_CREATE, location, name_token.value)

    def parse_channel_send(self) -> Optional[ChannelSend]:
        """Parse: Send "Hello" through messages."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "send")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "through")

        channel = self.parse_expression()
        if not channel:
            return None

        self.consume(TokenType.PERIOD)

        return ChannelSend(NodeType.CHANNEL_SEND, location, value, channel)

    def parse_channel_receive(self) -> Optional[ChannelReceive]:
        """Parse: Receive a message from messages and store it in message."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "receive")
        self.consume(TokenType.KEYWORD, "a")
        self.consume(TokenType.KEYWORD, "message")
        self.consume(TokenType.KEYWORD, "from")

        channel = self.parse_expression()
        if not channel:
            return None

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "it")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return ChannelReceive(NodeType.CHANNEL_RECEIVE, location, channel, variable_token.value)

    def parse_file_read(self) -> Optional[FileRead]:
        """Parse: Read the file "data.txt" into contents."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "read")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "file")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.KEYWORD, "into")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return FileRead(NodeType.FILE_READ, location, path, variable_token.value)

    def parse_file_write(self) -> Optional[FileWrite]:
        """Parse: Write contents to the file "output.txt"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "write")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "file")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.PERIOD)

        return FileWrite(NodeType.FILE_WRITE, location, value, path)

    def parse_file_append(self) -> Optional[FileAppend]:
        """Parse: Append "Hello" to the file "log.txt"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "append")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "file")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.PERIOD)

        return FileAppend(NodeType.FILE_APPEND, location, value, path)

    def parse_directory_create(self) -> Optional[DirectoryCreate]:
        """Parse: Create the directory "data"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "create")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "directory")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.PERIOD)

        return DirectoryCreate(NodeType.DIRECTORY_CREATE, location, path)

    def parse_directory_list(self) -> Optional[DirectoryList]:
        """Parse: List the files in the directory "data" and store them in files."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "list")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "files")
        self.consume(TokenType.KEYWORD, "in")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "directory")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "them")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return DirectoryList(NodeType.DIRECTORY_LIST, location, path, variable_token.value)

    def parse_file_delete(self) -> Optional[FileDelete]:
        """Parse: Delete the file "old.txt"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "delete")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "file")

        path = self.parse_expression()
        if not path:
            return None

        self.consume(TokenType.PERIOD)

        return FileDelete(NodeType.FILE_DELETE, location, path)

    def parse_env_get(self) -> Optional[EnvGet]:
        """Parse: Get the environment variable "HOME" and store it in home."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "get")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "environment")
        self.consume(TokenType.KEYWORD, "variable")

        name = self.parse_expression()
        if not name:
            return None

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "it")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return EnvGet(NodeType.ENV_GET, location, name, variable_token.value)

    def parse_env_set(self) -> Optional[EnvSet]:
        """Parse: Set the environment variable "MODE" to "production"."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "set")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "environment")
        self.consume(TokenType.KEYWORD, "variable")

        name = self.parse_expression()
        if not name:
            return None

        self.consume(TokenType.KEYWORD, "to")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.PERIOD)

        return EnvSet(NodeType.ENV_SET, location, name, value)

    def parse_command_run(self) -> Optional[CommandRun]:
        """Parse: Run the command "git" with arguments "status" and store the result in result."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "run")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "command")

        command = self.parse_expression()
        if not command:
            return None

        arguments: List[ASTNode] = []
        if self.match_keyword("with"):
            self.consume(TokenType.KEYWORD, "with")
            self.consume(TokenType.KEYWORD, "arguments")

            while True:
                arg = self.parse_expression()
                if not arg:
                    break
                arguments.append(arg)

                if self.check(TokenType.COMMA):
                    self.consume(TokenType.COMMA)
                elif self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                else:
                    break

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "result")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return CommandRun(NodeType.COMMAND_RUN, location, command, arguments, variable_token.value)

    def parse_shell_run(self) -> Optional[ShellRun]:
        """Parse: Run the shell command "echo hello" and store the result in result."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "run")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "shell")
        self.consume(TokenType.KEYWORD, "command")

        command = self.parse_expression()
        if not command:
            return None

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "result")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return ShellRun(NodeType.SHELL_RUN, location, command, variable_token.value)

    def parse_http_request(self) -> Optional[HttpRequest]:
        """Parse: Send a GET request to "https://example.com" and store the response in response."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "send")
        self.consume(TokenType.KEYWORD, "a")

        method_token = self.consume(TokenType.IDENTIFIER)
        if not method_token:
            return None

        method = method_token.value.upper()
        self.consume(TokenType.KEYWORD, "request")
        self.consume(TokenType.KEYWORD, "to")

        url = self.parse_expression()
        if not url:
            return None

        headers = None
        body = None

        # Check for headers
        if self.match_keyword("with"):
            self.consume(TokenType.KEYWORD, "with")
            if self.match_keyword("headers"):
                self.consume(TokenType.KEYWORD, "headers")
                headers = self.parse_expression()

        # Check for body
        if self.match_keyword("with"):
            self.consume(TokenType.KEYWORD, "with")
            if self.match_keyword("json"):
                self.consume(TokenType.KEYWORD, "json")
                self.consume(TokenType.KEYWORD, "containing")
                body = self.parse_expression()
            else:
                body = self.parse_expression()

        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "response")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return HttpRequest(NodeType.HTTP_REQUEST, location, method, url, headers, body, variable_token.value)

    def parse_json_parse(self) -> Optional[JsonParse]:
        """Parse: Parse response.body as JSON and store it in data."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "parse")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "as")
        self.consume(TokenType.KEYWORD, "json")
        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "it")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return JsonParse(NodeType.JSON_PARSE, location, value, variable_token.value)

    def parse_json_stringify(self) -> Optional[JsonStringify]:
        """Parse: Convert data to JSON and store it in json."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "convert")

        value = self.parse_expression()
        if not value:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "json")
        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "store")
        self.consume(TokenType.KEYWORD, "it")
        self.consume(TokenType.KEYWORD, "in")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.PERIOD)

        return JsonStringify(NodeType.JSON_STRINGIFY, location, value, variable_token.value)

    def parse_time_now(self) -> Optional[TimeNow]:
        """Parse: Set now to the current date and time."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "set")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "current")
        self.consume(TokenType.KEYWORD, "date")
        self.consume(TokenType.KEYWORD, "and")
        self.consume(TokenType.KEYWORD, "time")
        self.consume(TokenType.PERIOD)

        return TimeNow(NodeType.TIME_NOW, location, variable_token.value)

    def parse_time_timestamp(self) -> Optional[TimeTimestamp]:
        """Parse: Set timestamp to the current Unix timestamp."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "set")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "the")
        self.consume(TokenType.KEYWORD, "current")
        self.consume(TokenType.KEYWORD, "unix")
        self.consume(TokenType.KEYWORD, "timestamp")
        self.consume(TokenType.PERIOD)

        return TimeTimestamp(NodeType.TIME_TIMESTAMP, location, variable_token.value)

    def parse_time_sleep(self) -> Optional[TimeSleep]:
        """Parse: Wait for 2 seconds."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "wait")
        self.consume(TokenType.KEYWORD, "for")

        duration = self.parse_expression()
        if not duration:
            return None

        self.consume(TokenType.KEYWORD, "seconds")
        self.consume(TokenType.PERIOD)

        return TimeSleep(NodeType.TIME_SLEEP, location, duration)

    def parse_random_number(self) -> Optional[RandomNumber]:
        """Parse: Set number to a random number between 1 and 100."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "set")

        variable_token = self.consume(TokenType.IDENTIFIER)
        if not variable_token:
            return None

        self.consume(TokenType.KEYWORD, "to")
        self.consume(TokenType.KEYWORD, "a")
        self.consume(TokenType.KEYWORD, "random")
        self.consume(TokenType.KEYWORD, "number")
        self.consume(TokenType.KEYWORD, "between")

        min_val = self.parse_expression()
        if not min_val:
            return None

        self.consume(TokenType.KEYWORD, "and")

        max_val = self.parse_expression()
        if not max_val:
            return None

        self.consume(TokenType.PERIOD)

        return RandomNumber(NodeType.RANDOM_NUMBER, location, min_val, max_val, variable_token.value)

    def parse_object_literal(self) -> Optional[ObjectLiteral]:
        """Parse: Create an object called player."""
        location = self.current_token().location
        self.consume(TokenType.KEYWORD, "create")
        self.consume(TokenType.KEYWORD, "an")
        self.consume(TokenType.KEYWORD, "object")
        self.consume(TokenType.KEYWORD, "called")

        name_token = self.consume(TokenType.IDENTIFIER)
        if not name_token:
            return None

        self.consume(TokenType.PERIOD)

        return ObjectLiteral(NodeType.OBJECT_LITERAL, location, name_token.value)

    def parse_block(self) -> List[ASTNode]:
        """Parse a block of statements."""
        statements: List[ASTNode] = []

        # Consume INDENT if present
        if self.check(TokenType.INDENT):
            self.advance()

        self.skip_newlines()

        while self.current_token() and self.current_token().type != TokenType.EOF:
            # Check for dedent (end of block)
            if self.check(TokenType.DEDENT):
                self.advance()  # Consume the DEDENT
                break

            # Skip any additional INDENT tokens (in case of issues)
            while self.check(TokenType.INDENT):
                self.advance()

            # Check for keywords that end blocks (only in specific contexts)
            # Don't break on "end" keywords here - let the parent handle them
            if self.match_keyword("otherwise", "when"):
                break

            self.skip_newlines()

            if self.current_token() and self.current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                else:
                    # If we couldn't parse a statement, advance to avoid infinite loop
                    self.advance()

                self.skip_newlines()

        return statements

    def parse_function_call(self, function: Identifier) -> Optional[Call]:
        """Parse: function with arg1 and arg2."""
        location = function.location
        self.consume(TokenType.KEYWORD, "with")

        arguments: List[ASTNode] = []
        while True:
            # Parse the argument - for function calls, "and" is a separator, not an operator
            # So we parse it specially
            arg = self.parse_primary()
            if not arg:
                break
            
            # Check if this could be a binary expression like "n minus 1"
            # We only allow this if it's NOT followed by "and" (which would be a separator)
            if not self.check(TokenType.KEYWORD, "and") and not self.check(TokenType.PERIOD):
                # Try to parse as a binary expression (but not with "and" as operator)
                op = self.get_binary_operator()
                if op and op != "and":
                    self.consume_operator_tokens(op)
                    right = self.parse_binary_operation(self.get_operator_precedence(op) + 1)
                    if right:
                        arg = BinaryOperation(NodeType.BINARY_OPERATION, arg.location, op, arg, right)
            
            arguments.append(arg)

            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
                # After comma, there might be "and" as the next separator
                if self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next argument
                continue
            elif self.check(TokenType.KEYWORD, "and"):
                # In function call context, "and" is an argument separator, not a boolean operator
                self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next argument
                continue
            elif self.check(TokenType.PERIOD):
                # Don't consume the period - let the statement parser handle it
                break
            else:
                break

        return Call(NodeType.CALL, location, function, arguments)

    def parse_expression(self) -> Optional[ASTNode]:
        """Parse an expression."""
        return self.parse_binary_operation(0)

    def parse_binary_operation(self, precedence: int) -> Optional[ASTNode]:
        """Parse a binary operation with operator precedence."""
        left = self.parse_unary_operation()
        if not left:
            return None

        while True:
            op = self.get_binary_operator()
            if not op:
                break

            op_prec = self.get_operator_precedence(op)
            if op_prec < precedence:
                break

            self.consume_operator_tokens(op)

            right = self.parse_binary_operation(op_prec + 1)
            if not right:
                break

            left = BinaryOperation(NodeType.BINARY_OPERATION, left.location, op, left, right)

        return left

    def parse_unary_operation(self) -> Optional[ASTNode]:
        """Parse a unary operation."""
        if self.match_keyword("not"):
            location = self.current_token().location
            self.consume(TokenType.KEYWORD, "not")
            operand = self.parse_unary_operation()
            if not operand:
                return None
            return UnaryOperation(NodeType.UNARY_OPERATION, location, "not", operand)

        expr = self.parse_primary()
        if not expr:
            return None

        # Check for function call: identifier with arg1 and arg2
        if self.check(TokenType.KEYWORD, "with"):
            if isinstance(expr, Identifier):
                return self.parse_function_call(expr)

        return expr

    def parse_primary(self) -> Optional[ASTNode]:
        """Parse a primary expression."""
        token = self.current_token()
        if token is None:
            return None

        # Literal
        if token.type == TokenType.NUMBER:
            self.advance()
            try:
                if "." in token.value:
                    value = float(token.value)
                else:
                    value = int(token.value)
            except ValueError:
                value = 0
            return Literal(NodeType.LITERAL, token.location, value)

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(NodeType.LITERAL, token.location, token.value)

        if token.type == TokenType.BOOLEAN:
            self.advance()
            value = token.value.lower() in ["true", "yes"]
            return Literal(NodeType.LITERAL, token.location, value)

        if self.match_keyword("nothing"):
            location = self.current_token().location
            self.consume(TokenType.KEYWORD, "nothing")
            return Literal(NodeType.LITERAL, location, None)

        # Parenthesized expression
        if token.type == TokenType.LEFT_PAREN:
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RIGHT_PAREN)
            return expr

        # List literal
        if self.check(TokenType.KEYWORD, "a"):
            if self.peek_token() and self.peek_token().value.lower() == "list":
                self.consume(TokenType.KEYWORD, "a")
                return self.parse_list_literal()

        # Map literal
        if self.check(TokenType.KEYWORD, "a"):
            if self.peek_token() and self.peek_token().value.lower() == "map":
                self.consume(TokenType.KEYWORD, "a")
                return self.parse_map_literal()

        # Set literal
        if self.check(TokenType.KEYWORD, "a"):
            if self.peek_token() and self.peek_token().value.lower() == "set":
                self.consume(TokenType.KEYWORD, "a")
                return self.parse_set_literal()

        # Type construction
        if self.check(TokenType.KEYWORD, "a"):
            if self.peek_token() and self.peek_token().type == TokenType.IDENTIFIER:
                self.consume(TokenType.KEYWORD, "a")
                return self.parse_type_construction()

        # Identifier
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(NodeType.IDENTIFIER, token.location, token.value)

        # String interpolation
        if token.type == TokenType.STRING and "{" in token.value:
            self.advance()
            return self.parse_string_interpolation(token.value, token.location)

        self.error(f"Unexpected token in expression: {token.value}")
        return None

    def parse_list_literal(self) -> Optional[ListLiteral]:
        """Parse: a list containing 1, 2, and 3."""
        location = self.current_token().location
        # "a" already consumed
        self.consume(TokenType.KEYWORD, "list")
        self.consume(TokenType.KEYWORD, "containing")

        elements: List[ASTNode] = []
        while True:
            # Parse a single literal value (not a full expression to avoid binary ops)
            elem = self.parse_primary()
            if not elem:
                break
            elements.append(elem)

            # Check for separator
            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
                # After comma, there might be "and" as the next separator
                if self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                # Continue to next element
                continue
            elif self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")
                # Continue to next element
                continue
            elif self.check(TokenType.PERIOD):
                # Consume the period since we've finished the list
                self.consume(TokenType.PERIOD)
                break
            else:
                # No more elements
                break

        return ListLiteral(NodeType.LIST_LITERAL, location, elements)

    def parse_map_literal(self) -> Optional[MapLiteral]:
        """Parse: a map containing "name" mapped to "AB", "age" mapped to 20."""
        location = self.current_token().location
        # "a" already consumed
        self.consume(TokenType.KEYWORD, "map")
        self.consume(TokenType.KEYWORD, "containing")
        self.consume(TokenType.COLON)

        pairs: List[tuple] = []
        while not self.check(TokenType.EOF):
            key = self.parse_expression()
            if not key:
                break

            self.consume(TokenType.KEYWORD, "mapped")
            self.consume(TokenType.KEYWORD, "to")

            value = self.parse_expression()
            if not value:
                break

            pairs.append((key, value))

            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
                # After comma, there might be "and" as the next separator
                if self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next pair
                continue
            elif self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next pair
                continue
            elif self.check(TokenType.PERIOD):
                # Stop at period
                self.consume(TokenType.PERIOD)
                break
            else:
                break

        return MapLiteral(NodeType.MAP_LITERAL, location, pairs)

    def parse_set_literal(self) -> Optional[SetLiteral]:
        """Parse: a set containing 1, 2, and 3."""
        location = self.current_token().location
        # "a" already consumed
        self.consume(TokenType.KEYWORD, "set")
        self.consume(TokenType.KEYWORD, "containing")

        elements: List[ASTNode] = []
        while True:
            elem = self.parse_expression()
            if not elem:
                break
            elements.append(elem)

            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
                # After comma, there might be "and" as the next separator
                if self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next element
                continue
            elif self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next element
                continue
            elif self.check(TokenType.PERIOD):
                # Stop at period
                self.consume(TokenType.PERIOD)
                break
            else:
                break

        return SetLiteral(NodeType.SET_LITERAL, location, elements)

    def parse_type_construction(self) -> Optional[TypeConstruction]:
        """Parse: a Player with name equal to "Hero"."""
        location = self.current_token().location
        # "a" already consumed

        type_name_token = self.consume(TokenType.IDENTIFIER)
        if not type_name_token:
            return None

        self.consume(TokenType.KEYWORD, "with")

        fields: List[tuple] = []
        while True:
            field_name = self.consume(TokenType.IDENTIFIER)
            if not field_name:
                break

            self.consume(TokenType.KEYWORD, "equal")
            self.consume(TokenType.KEYWORD, "to")

            field_value = self.parse_expression()
            if not field_value:
                break

            fields.append((field_name.value, field_value))

            if self.check(TokenType.COMMA):
                self.consume(TokenType.COMMA)
                # After comma, there might be "and" as the next separator
                if self.check(TokenType.KEYWORD, "and"):
                    self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next field
                continue
            elif self.check(TokenType.KEYWORD, "and"):
                self.consume(TokenType.KEYWORD, "and")
                # Continue to parse next field
                continue
            elif self.check(TokenType.PERIOD):
                # Stop at period
                self.consume(TokenType.PERIOD)
                break
            else:
                break

        return TypeConstruction(NodeType.TYPE_CONSTRUCTION, location, type_name_token.value, fields)

    def parse_string_interpolation(self, value: str, location: SourceLocation) -> StringInterpolation:
        """Parse a string with interpolation."""
        parts: List[Union[str, ASTNode]] = []
        current = ""
        i = 0

        while i < len(value):
            if value[i] == "{" and i + 1 < len(value) and value[i + 1] == "{":
                # Escaped {{
                current += "{"
                i += 2
            elif value[i] == "{" and i + 1 < len(value) and value[i + 1] != "{":
                # Start of interpolation
                if current:
                    parts.append(current)
                    current = ""

                i += 1
                end = value.find("}", i)
                if end == -1:
                    current += "{"
                    i += 1
                    continue

                expr_str = value[i:end]
                # Parse the expression (simplified - in reality would need full parsing)
                parts.append(Identifier(NodeType.IDENTIFIER, location, expr_str.strip()))
                i = end + 1
            else:
                current += value[i]
                i += 1

        if current:
            parts.append(current)

        return StringInterpolation(NodeType.STRING_INTERPOLATION, location, parts)

    def get_binary_operator(self) -> Optional[str]:
        """Get the current binary operator."""
        token = self.current_token()
        if token is None:
            return None

        # Comparisons (check first since they start with "is")
        # IMPORTANT: Check longer operators first to avoid partial matches
        if self.check(TokenType.KEYWORD, "is"):
            # Check for "is less than or equal to" (6 words: is, less, than, or, equal, to)
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "less" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "than" and
                self.peek_token(3) and self.peek_token(3).value.lower() == "or" and
                self.peek_token(4) and self.peek_token(4).value.lower() == "equal" and
                self.peek_token(5) and self.peek_token(5).value.lower() == "to"):
                return "is less than or equal to"
            # Check for "is greater than or equal to" (6 words: is, greater, than, or, equal, to)
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "greater" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "than" and
                self.peek_token(3) and self.peek_token(3).value.lower() == "or" and
                self.peek_token(4) and self.peek_token(4).value.lower() == "equal" and
                self.peek_token(5) and self.peek_token(5).value.lower() == "to"):
                return "is greater than or equal to"
            # Check for "is not equal to" (4 words)
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "not" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "equal" and
                self.peek_token(3) and self.peek_token(3).value.lower() == "to"):
                return "is not equal to"
            # Check for "is equal to" (3 words)
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "equal" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "to"):
                return "is equal to"
            # Check for "is less than" (3 words) - check AFTER "is less than or equal to"
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "less" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "than"):
                return "is less than"
            # Check for "is greater than" (3 words) - check AFTER "is greater than or equal to"
            if (self.peek_token(1) and self.peek_token(1).value.lower() == "greater" and
                self.peek_token(2) and self.peek_token(2).value.lower() == "than"):
                return "is greater than"

        # Arithmetic
        if self.check(TokenType.KEYWORD, "plus"):
            return "plus"
        if self.check(TokenType.KEYWORD, "minus"):
            return "minus"
        if self.check(TokenType.KEYWORD, "multiplied"):
            if self.peek_token(1) and self.peek_token(1).value.lower() == "by":
                return "multiplied by"
        if self.check(TokenType.KEYWORD, "divided"):
            if self.peek_token(1) and self.peek_token(1).value.lower() == "by":
                return "divided by"
        if self.check(TokenType.KEYWORD, "modulo"):
            return "modulo"

        # Boolean
        if self.check(TokenType.KEYWORD, "and"):
            return "and"
        if self.check(TokenType.KEYWORD, "or"):
            return "or"

        return None

    def consume_operator_tokens(self, op: str) -> None:
        """Consume tokens for a multi-word operator."""
        parts = op.split()
        for part in parts:
            self.consume(TokenType.KEYWORD, part)

    def get_operator_precedence(self, op: str) -> int:
        """Get operator precedence (higher = tighter binding)."""
        precedence = {
            "and": 1,
            "or": 1,
            "is equal to": 2,
            "is not equal to": 2,
            "is greater than": 2,
            "is less than": 2,
            "is greater than or equal to": 2,
            "is less than or equal to": 2,
            "plus": 3,
            "minus": 3,
            "multiplied by": 4,
            "divided by": 4,
            "modulo": 4,
        }
        return precedence.get(op, 0)

    def get_errors(self) -> List[ParseError]:
        """Get all parse errors."""
        return self.errors
