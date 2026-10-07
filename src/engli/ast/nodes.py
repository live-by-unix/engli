from __future__ import annotations

"""
AST nodes for the Engli programming language.
"""

from dataclasses import dataclass
from typing import Any, Optional, List, Union
from enum import Enum

from ..lexer.tokens import SourceLocation


class NodeType(Enum):
    """Types of AST nodes."""

    # Program
    PROGRAM = "Program"

    # Statements
    VARIABLE_DECLARATION = "VariableDeclaration"
    VARIABLE_ASSIGNMENT = "VariableAssignment"
    ARITHMETIC_ASSIGNMENT = "ArithmeticAssignment"
    CONSTANT_DECLARATION = "ConstantDeclaration"
    FUNCTION_DECLARATION = "FunctionDeclaration"
    TYPE_DECLARATION = "TypeDeclaration"
    ENUM_DECLARATION = "EnumDeclaration"
    EXPORT = "Export"
    IMPORT = "Import"

    # Control flow
    IF_STATEMENT = "IfStatement"
    WHILE_LOOP = "WhileLoop"
    FOR_LOOP = "ForLoop"
    FOR_RANGE_LOOP = "ForRangeLoop"
    REPEAT_LOOP = "RepeatLoop"
    FOREVER_LOOP = "ForeverLoop"
    BREAK = "Break"
    CONTINUE = "Continue"
    MATCH_STATEMENT = "MatchStatement"
    MATCH_CASE = "MatchCase"

    # Try/catch
    TRY_STATEMENT = "TryStatement"

    # I/O
    SAY = "Say"
    ASK = "Ask"

    # Concurrency
    TASK_START = "TaskStart"
    TASK_WAIT = "TaskWait"
    CHANNEL_CREATE = "ChannelCreate"
    CHANNEL_SEND = "ChannelSend"
    CHANNEL_RECEIVE = "ChannelReceive"

    # Expressions
    LITERAL = "Literal"
    IDENTIFIER = "Identifier"
    BINARY_OPERATION = "BinaryOperation"
    UNARY_OPERATION = "UnaryOperation"
    CALL = "Call"
    PROPERTY_ACCESS = "PropertyAccess"
    INDEX_ACCESS = "IndexAccess"
    LIST_LITERAL = "ListLiteral"
    MAP_LITERAL = "MapLiteral"
    SET_LITERAL = "SetLiteral"
    OBJECT_LITERAL = "ObjectLiteral"
    TYPE_CONSTRUCTION = "TypeConstruction"
    ENUM_MEMBER = "EnumMember"
    OPTIONAL = "Optional"
    STRING_INTERPOLATION = "StringInterpolation"

    # Returns
    RETURN = "Return"

    # Filesystem
    FILE_READ = "FileRead"
    FILE_WRITE = "FileWrite"
    FILE_APPEND = "FileAppend"
    FILE_EXISTS = "FileExists"
    DIRECTORY_CREATE = "DirectoryCreate"
    DIRECTORY_LIST = "DirectoryList"
    FILE_DELETE = "FileDelete"

    # Environment
    ENV_GET = "EnvGet"
    ENV_SET = "EnvSet"

    # Process
    COMMAND_RUN = "CommandRun"
    SHELL_RUN = "ShellRun"

    # HTTP
    HTTP_REQUEST = "HttpRequest"
    JSON_PARSE = "JsonParse"
    JSON_STRINGIFY = "JsonStringify"

    # Time
    TIME_NOW = "TimeNow"
    TIME_TIMESTAMP = "TimeTimestamp"
    TIME_SLEEP = "TimeSleep"

    # Random
    RANDOM_NUMBER = "RandomNumber"

    # Object mutation
    PROPERTY_ASSIGNMENT = "PropertyAssignment"
    INDEX_ASSIGNMENT = "IndexAssignment"
    LIST_ADD = "ListAdd"
    LIST_REMOVE = "ListRemove"


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    node_type: NodeType
    location: SourceLocation


@dataclass
class Program(ASTNode):
    """The root node of an Engli program."""

    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    """Variable declaration: Set x to 10."""

    name: str
    value: ASTNode


@dataclass
class VariableAssignment(ASTNode):
    """Variable assignment: Set x to 20."""

    name: str
    value: ASTNode


@dataclass
class ArithmeticAssignment(ASTNode):
    """Arithmetic assignment: Add 5 to x."""

    operator: str  # "add", "subtract", "multiply", "divide", "modulo"
    name: str
    value: ASTNode


@dataclass
class ConstantDeclaration(ASTNode):
    """Constant declaration: Define the constant MAX as 100."""

    name: str
    value: ASTNode


@dataclass
class FunctionDeclaration(ASTNode):
    """Function declaration: Define a function called add that takes a and b: ..."""

    name: str
    parameters: List[str]
    body: List[ASTNode]


@dataclass
class TypeDeclaration(ASTNode):
    """Type declaration: Define a type called Player: ..."""

    name: str
    fields: List[tuple]  # (name, type_name)


@dataclass
class EnumDeclaration(ASTNode):
    """Enum declaration: Define an enumeration called Direction containing: ..."""

    name: str
    members: List[str]


@dataclass
class Export(ASTNode):
    """Export statement: Export function_name."""

    name: str


@dataclass
class Import(ASTNode):
    """Import statement: Import square from the file "./math.engli"."""

    path: str
    name: Optional[str] = None  # If None, import entire module


@dataclass
class IfStatement(ASTNode):
    """If statement: If condition: ... Otherwise if: ... Otherwise: ..."""

    condition: ASTNode
    then_block: List[ASTNode]
    elif_blocks: List[tuple]  # (condition, block)
    else_block: Optional[List[ASTNode]]


@dataclass
class WhileLoop(ASTNode):
    """While loop: While condition: ... End the loop."""

    condition: ASTNode
    body: List[ASTNode]


@dataclass
class ForLoop(ASTNode):
    """For loop: For each item in items: ..."""

    variable: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class ForRangeLoop(ASTNode):
    """For range loop: For each number from 1 through 10: ..."""

    variable: str
    start: ASTNode
    end: ASTNode
    body: List[ASTNode]


@dataclass
class RepeatLoop(ASTNode):
    """Repeat loop: Repeat 10 times: ..."""

    count: ASTNode
    body: List[ASTNode]


@dataclass
class ForeverLoop(ASTNode):
    """Forever loop: Forever: ..."""

    body: List[ASTNode]


@dataclass
class Break(ASTNode):
    """Break statement: Break out of the loop."""


@dataclass
class Continue(ASTNode):
    """Continue statement: Continue with the next iteration."""


@dataclass
class MatchStatement(ASTNode):
    """Match statement: Match value: When condition: ... Otherwise: ..."""

    value: ASTNode
    cases: List[tuple]  # (condition, body)
    default_case: Optional[List[ASTNode]]


@dataclass
class TryStatement(ASTNode):
    """Try statement: Try: ... If an error occurs as error: ..."""

    try_block: List[ASTNode]
    error_name: str
    catch_block: List[ASTNode]


@dataclass
class Say(ASTNode):
    """Say statement: Say "Hello"."""

    value: ASTNode


@dataclass
class Ask(ASTNode):
    """Ask statement: Ask the user for their name and store the answer in name."""

    prompt: ASTNode
    variable: str


@dataclass
class TaskStart(ASTNode):
    """Task start: Start a task: ..."""

    body: List[ASTNode]


@dataclass
class TaskWait(ASTNode):
    """Task wait: Wait for task to finish."""

    task: ASTNode


@dataclass
class ChannelCreate(ASTNode):
    """Channel create: Create a channel called messages."""

    name: str


@dataclass
class ChannelSend(ASTNode):
    """Channel send: Send "Hello" through messages."""

    value: ASTNode
    channel: ASTNode


@dataclass
class ChannelReceive(ASTNode):
    """Channel receive: Receive a message from messages and store it in message."""

    channel: ASTNode
    variable: str


@dataclass
class Literal(ASTNode):
    """Literal value: 10, "hello", true, nothing."""

    value: Any


@dataclass
class Identifier(ASTNode):
    """Identifier reference: x, name, function_name."""

    name: str


@dataclass
class BinaryOperation(ASTNode):
    """Binary operation: a plus b, x is greater than y."""

    operator: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOperation(ASTNode):
    """Unary operation: not x."""

    operator: str
    operand: ASTNode


@dataclass
class Call(ASTNode):
    """Function call: add with 10 and 20."""

    function: ASTNode
    arguments: List[ASTNode]


@dataclass
class PropertyAccess(ASTNode):
    """Property access: player.name."""

    object: ASTNode
    property: str


@dataclass
class IndexAccess(ASTNode):
    """Index access: numbers at index 0."""

    object: ASTNode
    index: ASTNode


@dataclass
class ListLiteral(ASTNode):
    """List literal: a list containing 1, 2, and 3."""

    elements: List[ASTNode]


@dataclass
class MapLiteral(ASTNode):
    """Map literal: a map containing "name" mapped to "AB", "age" mapped to 20."""

    pairs: List[tuple]  # (key, value)


@dataclass
class SetLiteral(ASTNode):
    """Set literal: a set containing 1, 2, and 3."""

    elements: List[ASTNode]


@dataclass
class ObjectLiteral(ASTNode):
    """Object literal: Create an object called player."""

    name: str


@dataclass
class TypeConstruction(ASTNode):
    """Type construction: Set player to a Player with name equal to "Hero"."""

    type_name: str
    fields: List[tuple]  # (field_name, value)


@dataclass
class EnumMember(ASTNode):
    """Enum member: Direction.North."""

    enum_name: str
    member: str


@dataclass
class Optional(ASTNode):
    """Optional value: username or "Guest"."""

    value: ASTNode
    default: ASTNode


@dataclass
class StringInterpolation(ASTNode):
    """String interpolation: "Hello, {name}."."""

    parts: List[Union[str, ASTNode]]


@dataclass
class Return(ASTNode):
    """Return statement: Return x."""

    value: Optional[ASTNode]


@dataclass
class PropertyAssignment(ASTNode):
    """Property assignment: Set player.name to "Hero"."""

    object: ASTNode
    property: str
    value: ASTNode


@dataclass
class IndexAssignment(ASTNode):
    """Index assignment: Set numbers at index 0 to 100."""

    object: ASTNode
    index: ASTNode
    value: ASTNode


@dataclass
class ListAdd(ASTNode):
    """List add: Add 6 to numbers."""

    list: ASTNode
    value: ASTNode


@dataclass
class ListRemove(ASTNode):
    """List remove: Remove 3 from numbers."""

    list: ASTNode
    value: ASTNode


@dataclass
class FileRead(ASTNode):
    """File read: Read the file "data.txt" into contents."""

    path: ASTNode
    variable: str


@dataclass
class FileWrite(ASTNode):
    """File write: Write contents to the file "output.txt"."""

    value: ASTNode
    path: ASTNode


@dataclass
class FileAppend(ASTNode):
    """File append: Append "Hello" to the file "log.txt"."""

    value: ASTNode
    path: ASTNode


@dataclass
class FileExists(ASTNode):
    """File exists: If the file "data.txt" exists: ..."""

    path: ASTNode


@dataclass
class DirectoryCreate(ASTNode):
    """Directory create: Create the directory "data"."""

    path: ASTNode


@dataclass
class DirectoryList(ASTNode):
    """Directory list: List the files in the directory "data" and store them in files."""

    path: ASTNode
    variable: str


@dataclass
class FileDelete(ASTNode):
    """File delete: Delete the file "old.txt"."""

    path: ASTNode


@dataclass
class EnvGet(ASTNode):
    """Environment variable get: Get the environment variable "HOME" and store it in home."""

    name: ASTNode
    variable: str


@dataclass
class EnvSet(ASTNode):
    """Environment variable set: Set the environment variable "MODE" to "production"."""

    name: ASTNode
    value: ASTNode


@dataclass
class CommandRun(ASTNode):
    """Command run: Run the command "git" with arguments "status" and store the result in result."""

    command: ASTNode
    arguments: List[ASTNode]
    variable: str


@dataclass
class ShellRun(ASTNode):
    """Shell run: Run the shell command "echo hello" and store the result in result."""

    command: ASTNode
    variable: str


@dataclass
class HttpRequest(ASTNode):
    """HTTP request: Send a GET request to "https://example.com" and store the response in response."""

    method: str  # GET, POST, PUT, PATCH, DELETE
    url: ASTNode
    headers: Optional[ASTNode]  # Map literal
    body: Optional[ASTNode]  # String or map
    variable: str


@dataclass
class JsonParse(ASTNode):
    """JSON parse: Parse response.body as JSON and store it in data."""

    value: ASTNode
    variable: str


@dataclass
class JsonStringify(ASTNode):
    """JSON stringify: Convert data to JSON and store it in json."""

    value: ASTNode
    variable: str


@dataclass
class TimeNow(ASTNode):
    """Time now: Set now to the current date and time."""

    variable: str


@dataclass
class TimeTimestamp(ASTNode):
    """Time timestamp: Set timestamp to the current Unix timestamp."""

    variable: str


@dataclass
class TimeSleep(ASTNode):
    """Time sleep: Wait for 2 seconds."""

    duration: ASTNode


@dataclass
class RandomNumber(ASTNode):
    """Random number: Set number to a random number between 1 and 100."""

    min: ASTNode
    max: ASTNode
    variable: str
