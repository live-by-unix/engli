from __future__ import annotations

"""
Interpreter for the Engli programming language.
"""

import sys
import json
from typing import Optional, List, Any, Dict
from pathlib import Path

from ..ast import *
from ..lexer.tokens import SourceLocation
from .values import Value, ValueType, create_number, create_decimal, create_text, create_boolean, create_nothing, create_list, create_map, create_set, create_error
from .environment import Environment
from .functions import EngliFunction, BuiltinFunction, create_builtin_function
from .objects import EngliObject
from .control_flow import ReturnValue, BreakException, ContinueException
from .errors import EngliRuntimeError


class Interpreter:
    """Interprets Engli AST nodes."""

    def __init__(self, environment: Optional[Environment] = None):
        self.environment = environment or Environment()
        self.stack_trace: List[str] = []
        self.current_loop_depth = 0
        self.modules: Dict[str, Any] = {}  # Module cache

        # Register built-in functions
        self._register_builtins()

    def _register_builtins(self) -> None:
        """Register built-in functions."""
        # Length function
        def length_fn(args: List[Value]) -> Value:
            if len(args) != 1:
                return create_error("length() expects 1 argument")
            val = args[0]
            if val.type == ValueType.LIST:
                return create_number(len(val.value))
            if val.type == ValueType.MAP:
                return create_number(len(val.value))
            if val.type == ValueType.SET:
                return create_number(len(val.value))
            if val.type == ValueType.TEXT:
                return create_number(len(val.value))
            return create_error("length() expects a list, map, set, or text")

        self.environment.define("length", create_builtin_function("length", length_fn))

    def interpret(self, program: Program) -> Optional[Value]:
        """Interpret a program."""
        try:
            return self.execute_block(program.statements)
        except EngliRuntimeError as e:
            print(e, file=sys.stderr)
            return None
        except Exception as e:
            print(f"Internal error: {e}", file=sys.stderr)
            return None

    def execute_block(self, statements: List[ASTNode], env: Optional[Environment] = None) -> Optional[Value]:
        """Execute a block of statements."""
        previous_env = self.environment
        if env:
            self.environment = env

        result = None
        for stmt in statements:
            result = self.execute(stmt)
            if result is not None:
                if isinstance(result, ReturnValue):
                    return result.value
                break

        self.environment = previous_env
        return result

    def execute(self, node: ASTNode) -> Optional[Value]:
        """Execute an AST node."""
        if isinstance(node, VariableDeclaration):
            return self.execute_variable_declaration(node)
        if isinstance(node, VariableAssignment):
            return self.execute_variable_assignment(node)
        if isinstance(node, ArithmeticAssignment):
            return self.execute_arithmetic_assignment(node)
        if isinstance(node, ConstantDeclaration):
            return self.execute_constant_declaration(node)
        if isinstance(node, FunctionDeclaration):
            return self.execute_function_declaration(node)
        if isinstance(node, TypeDeclaration):
            return self.execute_type_declaration(node)
        if isinstance(node, EnumDeclaration):
            return self.execute_enum_declaration(node)
        if isinstance(node, Export):
            return self.execute_export(node)
        if isinstance(node, Import):
            return self.execute_import(node)
        if isinstance(node, IfStatement):
            return self.execute_if_statement(node)
        if isinstance(node, WhileLoop):
            return self.execute_while_loop(node)
        if isinstance(node, ForLoop):
            return self.execute_for_loop(node)
        if isinstance(node, ForRangeLoop):
            return self.execute_for_range_loop(node)
        if isinstance(node, RepeatLoop):
            return self.execute_repeat_loop(node)
        if isinstance(node, ForeverLoop):
            return self.execute_forever_loop(node)
        if isinstance(node, Break):
            return self.execute_break(node)
        if isinstance(node, Continue):
            return self.execute_continue(node)
        if isinstance(node, MatchStatement):
            return self.execute_match_statement(node)
        if isinstance(node, TryStatement):
            return self.execute_try_statement(node)
        if isinstance(node, Say):
            return self.execute_say(node)
        if isinstance(node, Ask):
            return self.execute_ask(node)
        if isinstance(node, TaskStart):
            return self.execute_task_start(node)
        if isinstance(node, TaskWait):
            return self.execute_task_wait(node)
        if isinstance(node, ChannelCreate):
            return self.execute_channel_create(node)
        if isinstance(node, ChannelSend):
            return self.execute_channel_send(node)
        if isinstance(node, ChannelReceive):
            return self.execute_channel_receive(node)
        if isinstance(node, Return):
            return self.execute_return(node)
        if isinstance(node, PropertyAssignment):
            return self.execute_property_assignment(node)
        if isinstance(node, IndexAssignment):
            return self.execute_index_assignment(node)
        if isinstance(node, ListAdd):
            return self.execute_list_add(node)
        if isinstance(node, ListRemove):
            return self.execute_list_remove(node)
        if isinstance(node, FileRead):
            return self.execute_file_read(node)
        if isinstance(node, FileWrite):
            return self.execute_file_write(node)
        if isinstance(node, FileAppend):
            return self.execute_file_append(node)
        if isinstance(node, FileExists):
            return self.execute_file_exists(node)
        if isinstance(node, DirectoryCreate):
            return self.execute_directory_create(node)
        if isinstance(node, DirectoryList):
            return self.execute_directory_list(node)
        if isinstance(node, FileDelete):
            return self.execute_file_delete(node)
        if isinstance(node, EnvGet):
            return self.execute_env_get(node)
        if isinstance(node, EnvSet):
            return self.execute_env_set(node)
        if isinstance(node, CommandRun):
            return self.execute_command_run(node)
        if isinstance(node, ShellRun):
            return self.execute_shell_run(node)
        if isinstance(node, HttpRequest):
            return self.execute_http_request(node)
        if isinstance(node, JsonParse):
            return self.execute_json_parse(node)
        if isinstance(node, JsonStringify):
            return self.execute_json_stringify(node)
        if isinstance(node, TimeNow):
            return self.execute_time_now(node)
        if isinstance(node, TimeTimestamp):
            return self.execute_time_timestamp(node)
        if isinstance(node, TimeSleep):
            return self.execute_time_sleep(node)
        if isinstance(node, RandomNumber):
            return self.execute_random_number(node)
        if isinstance(node, ObjectLiteral):
            return self.execute_object_literal(node)
        if isinstance(node, Call):
            return self.execute_call(node)

        # Expressions as statements
        if isinstance(node, BinaryOperation):
            self.evaluate(node)
            return None
        if isinstance(node, UnaryOperation):
            self.evaluate(node)
            return None
        if isinstance(node, Literal):
            self.evaluate(node)
            return None
        if isinstance(node, Identifier):
            self.evaluate(node)
            return None

        self.error(f"Unknown node type: {node.node_type}", node.location)
        return None

    def evaluate(self, node: ASTNode) -> Value:
        """Evaluate an expression node."""
        if isinstance(node, Literal):
            return self.evaluate_literal(node)
        if isinstance(node, Identifier):
            return self.evaluate_identifier(node)
        if isinstance(node, BinaryOperation):
            return self.evaluate_binary_operation(node)
        if isinstance(node, UnaryOperation):
            return self.evaluate_unary_operation(node)
        if isinstance(node, Call):
            return self.evaluate_call(node)
        if isinstance(node, PropertyAccess):
            return self.evaluate_property_access(node)
        if isinstance(node, IndexAccess):
            return self.evaluate_index_access(node)
        if isinstance(node, ListLiteral):
            return self.evaluate_list_literal(node)
        if isinstance(node, MapLiteral):
            return self.evaluate_map_literal(node)
        if isinstance(node, SetLiteral):
            return self.evaluate_set_literal(node)
        if isinstance(node, ObjectLiteral):
            return self.evaluate_object_literal(node)
        if isinstance(node, TypeConstruction):
            return self.evaluate_type_construction(node)
        if isinstance(node, EnumMember):
            return self.evaluate_enum_member(node)
        if isinstance(node, Optional):
            return self.evaluate_optional(node)
        if isinstance(node, StringInterpolation):
            return self.evaluate_string_interpolation(node)

        self.error(f"Cannot evaluate node type: {node.node_type}", node.location)
        return create_error(f"Cannot evaluate: {node.node_type}")

    def execute_variable_declaration(self, node: VariableDeclaration) -> Optional[Value]:
        """Execute: Set x to 10."""
        value = self.evaluate(node.value)
        self.environment.define(node.name, value)
        return None

    def execute_variable_assignment(self, node: VariableAssignment) -> Optional[Value]:
        """Execute: Set x to 20."""
        value = self.evaluate(node.value)
        if not self.environment.assign(node.name, value):
            self.error(f"Undefined variable: {node.name}", node.location)
        return None

    def execute_arithmetic_assignment(self, node: ArithmeticAssignment) -> Optional[Value]:
        """Execute: Add 5 to x."""
        current = self.environment.get(node.name)
        if current is None:
            self.error(f"Undefined variable: {node.name}", node.location)
            return None

        value = self.evaluate(node.value)

        # If the target is a list, treat "add" as list append
        if current.type == ValueType.LIST:
            current.value.append(value)
            return None

        if node.operator == "add":
            if current.type == ValueType.NUMBER and value.type == ValueType.NUMBER:
                result = create_number(current.value + value.value)
            elif current.type == ValueType.DECIMAL or value.type == ValueType.DECIMAL:
                result = create_decimal(float(current.value) + float(value.value))
            else:
                self.error("Cannot add these types", node.location)
                return None
        elif node.operator == "subtract":
            if current.type == ValueType.NUMBER and value.type == ValueType.NUMBER:
                result = create_number(current.value - value.value)
            elif current.type == ValueType.DECIMAL or value.type == ValueType.DECIMAL:
                result = create_decimal(float(current.value) - float(value.value))
            else:
                self.error("Cannot subtract these types", node.location)
                return None
        elif node.operator == "multiply":
            if current.type == ValueType.NUMBER and value.type == ValueType.NUMBER:
                result = create_number(current.value * value.value)
            elif current.type == ValueType.DECIMAL or value.type == ValueType.DECIMAL:
                result = create_decimal(float(current.value) * float(value.value))
            else:
                self.error("Cannot multiply these types", node.location)
                return None
        elif node.operator == "divide":
            if current.type == ValueType.NUMBER and value.type == ValueType.NUMBER:
                if value.value == 0:
                    self.error("Division by zero", node.location)
                    return None
                result = create_number(current.value // value.value)
            elif current.type == ValueType.DECIMAL or value.type == ValueType.DECIMAL:
                if float(value.value) == 0:
                    self.error("Division by zero", node.location)
                    return None
                result = create_decimal(float(current.value) / float(value.value))
            else:
                self.error("Cannot divide these types", node.location)
                return None
        elif node.operator == "modulo":
            if current.type == ValueType.NUMBER and value.type == ValueType.NUMBER:
                if value.value == 0:
                    self.error("Modulo by zero", node.location)
                    return None
                result = create_number(current.value % value.value)
            elif current.type == ValueType.DECIMAL or value.type == ValueType.DECIMAL:
                if float(value.value) == 0:
                    self.error("Modulo by zero", node.location)
                    return None
                result = create_decimal(float(current.value) % float(value.value))
            else:
                self.error("Cannot modulo these types", node.location)
                return None
        else:
            self.error(f"Unknown arithmetic operator: {node.operator}", node.location)
            return None

        self.environment.assign(node.name, result)
        return None

    def execute_constant_declaration(self, node: ConstantDeclaration) -> Optional[Value]:
        """Execute: Define the constant MAX as 100."""
        value = self.evaluate(node.value)
        self.environment.define(node.name, value, is_constant=True)
        return None

    def execute_function_declaration(self, node: FunctionDeclaration) -> Optional[Value]:
        """Execute: Define a function called add that takes a and b: ..."""
        func = EngliFunction(node.name, node.parameters, node.body, self.environment, self)
        self.environment.define(node.name, Value(ValueType.FUNCTION, func))
        return None

    def execute_type_declaration(self, node: TypeDeclaration) -> Optional[Value]:
        """Execute: Define a type called Player: ..."""
        # Store type definition in environment
        self.environment.define(node.name, Value(ValueType.TYPE, {"name": node.name, "fields": node.fields}))
        return None

    def execute_enum_declaration(self, node: EnumDeclaration) -> Optional[Value]:
        """Execute: Define an enumeration called Direction containing: ..."""
        # Store enum definition in environment
        self.environment.define(node.name, Value(ValueType.ENUM, {"name": node.name, "members": node.members}))
        return None

    def execute_export(self, node: Export) -> Optional[Value]:
        """Execute: Export function_name."""
        # In a module system, this would mark the symbol for export
        # For now, we just note it in the environment
        self.environment.define(f"__export_{node.name}", Value(ValueType.BOOLEAN, True))
        return None

    def execute_import(self, node: Import) -> Optional[Value]:
        """Execute: Import square from the file "./math.engli"."""
        # Resolve the path
        import_path = Path(node.path)
        if not import_path.is_absolute():
            # Get the current file's directory (would need to track this)
            import_path = Path.cwd() / import_path

        # Check cache
        cache_key = str(import_path)
        if cache_key in self.modules:
            module_env = self.modules[cache_key]
        else:
            # Load and execute the module
            from ..cli import load_source
            source = load_source(str(import_path))

            from ..lexer import Lexer
            from ..parser import Parser
            from ..ast import Program

            lexer = Lexer(source, str(import_path))
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            program = parser.parse()

            # Create a new environment for the module
            module_env = Environment(self.environment)
            module_interpreter = Interpreter(module_env)
            module_interpreter.interpret(program)

            self.modules[cache_key] = module_env
            module_env = module_env

        # Import the symbol
        if node.name:
            # Named import
            value = module_env.get(node.name)
            if value is None:
                self.error(f"Cannot import undefined symbol: {node.name}", node.location)
                return None
            self.environment.define(node.name, value)
        else:
            # Module import - import all non-private symbols
            for name, value in module_env.values.items():
                if not name.startswith("__"):
                    self.environment.define(name, value)

        return None

    def execute_if_statement(self, node: IfStatement) -> Optional[Value]:
        """Execute: If condition: ... Otherwise if: ... Otherwise: ..."""
        condition = self.evaluate(node.condition)

        if condition.is_truthy():
            return self.execute_block(node.then_block)

        for elif_condition, elif_block in node.elif_blocks:
            elif_cond = self.evaluate(elif_condition)
            if elif_cond.is_truthy():
                return self.execute_block(elif_block)

        if node.else_block:
            return self.execute_block(node.else_block)

        return None

    def execute_while_loop(self, node: WhileLoop) -> Optional[Value]:
        """Execute: While condition: ..."""
        self.current_loop_depth += 1
        try:
            while True:
                condition = self.evaluate(node.condition)
                if not condition.is_truthy():
                    break

                result = self.execute_block(node.body)
                if result is not None:
                    if isinstance(result, ReturnValue):
                        return result
                    break
        finally:
            self.current_loop_depth -= 1

        return None

    def execute_for_loop(self, node: ForLoop) -> Optional[Value]:
        """Execute: For each item in items: ..."""
        self.current_loop_depth += 1
        try:
            iterable = self.evaluate(node.iterable)

            if iterable.type != ValueType.LIST:
                self.error("For loop requires a list", node.location)
                return None

            for item in iterable.value:
                self.environment.define(node.variable, item)
                result = self.execute_block(node.body)
                if result is not None:
                    if isinstance(result, ReturnValue):
                        return result
                    break
        finally:
            self.current_loop_depth -= 1

        return None

    def execute_for_range_loop(self, node: ForRangeLoop) -> Optional[Value]:
        """Execute: For each number from 1 through 10: ..."""
        self.current_loop_depth += 1
        try:
            start = self.evaluate(node.start)
            end = self.evaluate(node.end)

            if start.type != ValueType.NUMBER or end.type != ValueType.NUMBER:
                self.error("For range loop requires numbers", node.location)
                return None

            for i in range(start.value, end.value + 1):
                self.environment.define(node.variable, create_number(i))
                result = self.execute_block(node.body)
                if result is not None:
                    if isinstance(result, ReturnValue):
                        return result
                    break
        finally:
            self.current_loop_depth -= 1

        return None

    def execute_repeat_loop(self, node: RepeatLoop) -> Optional[Value]:
        """Execute: Repeat 10 times: ..."""
        self.current_loop_depth += 1
        try:
            count = self.evaluate(node.count)

            if count.type != ValueType.NUMBER:
                self.error("Repeat loop requires a number", node.location)
                return None

            for _ in range(count.value):
                result = self.execute_block(node.body)
                if result is not None:
                    if isinstance(result, ReturnValue):
                        return result
                    break
        finally:
            self.current_loop_depth -= 1

        return None

    def execute_forever_loop(self, node: ForeverLoop) -> Optional[Value]:
        """Execute: Forever: ..."""
        self.current_loop_depth += 1
        try:
            while True:
                result = self.execute_block(node.body)
                if result is not None:
                    if isinstance(result, ReturnValue):
                        return result
                    break
        finally:
            self.current_loop_depth -= 1

        return None

    def execute_break(self, node: Break) -> Optional[Value]:
        """Execute: Break out of the loop."""
        if self.current_loop_depth == 0:
            self.error("Break outside of loop", node.location)
            return None
        raise BreakException()

    def execute_continue(self, node: Continue) -> Optional[Value]:
        """Execute: Continue with the next iteration."""
        if self.current_loop_depth == 0:
            self.error("Continue outside of loop", node.location)
            return None
        raise ContinueException()

    def execute_match_statement(self, node: MatchStatement) -> Optional[Value]:
        """Execute: Match value: When condition: ... Otherwise: ..."""
        value = self.evaluate(node.value)

        for condition, body in node.cases:
            # Evaluate the condition (simplified - should support pattern matching)
            cond_value = self.evaluate(condition)

            # Check if values match
            if self._values_equal(value, cond_value):
                return self.execute_block(body)

        if node.default_case:
            return self.execute_block(node.default_case)

        return None

    def _values_equal(self, a: Value, b: Value) -> bool:
        """Check if two values are equal."""
        if a.type != b.type:
            return False
        return a.value == b.value

    def execute_try_statement(self, node: TryStatement) -> Optional[Value]:
        """Execute: Try: ... If an error occurs as error: ..."""
        try:
            return self.execute_block(node.try_block)
        except Exception as e:
            error_value = create_error(str(e))
            self.environment.define(node.error_name, error_value)
            return self.execute_block(node.catch_block)

    def execute_say(self, node: Say) -> Optional[Value]:
        """Execute: Say "Hello"."""
        value = self.evaluate(node.value)
        print(self._value_to_string(value))
        return None

    def execute_ask(self, node: Ask) -> Optional[Value]:
        """Execute: Ask the user for their name and store the answer in name."""
        prompt = self._value_to_string(self.evaluate(node.prompt))
        answer = input(prompt)
        self.environment.define(node.variable, create_text(answer))
        return None

    def execute_task_start(self, node: TaskStart) -> Optional[Value]:
        """Execute: Start a task: ..."""
        # For now, execute synchronously
        # In a full implementation, this would use asyncio
        return self.execute_block(node.body)

    def execute_task_wait(self, node: TaskWait) -> Optional[Value]:
        """Execute: Wait for task to finish."""
        # For now, this is a no-op since tasks run synchronously
        return None

    def execute_channel_create(self, node: ChannelCreate) -> Optional[Value]:
        """Execute: Create a channel called messages."""
        # Create a simple queue
        import queue
        channel = queue.Queue()
        self.environment.define(node.name, Value(ValueType.MAP, {"queue": channel}))
        return None

    def execute_channel_send(self, node: ChannelSend) -> Optional[Value]:
        """Execute: Send "Hello" through messages."""
        value = self.evaluate(node.value)
        channel = self.evaluate(node.channel)

        if channel.type != ValueType.MAP or "queue" not in channel.value:
            self.error("Invalid channel", node.location)
            return None

        channel.value["queue"].put(value)
        return None

    def execute_channel_receive(self, node: ChannelReceive) -> Optional[Value]:
        """Execute: Receive a message from messages and store it in message."""
        channel = self.evaluate(node.channel)

        if channel.type != ValueType.MAP or "queue" not in channel.value:
            self.error("Invalid channel", node.location)
            return None

        value = channel.value["queue"].get()
        self.environment.define(node.variable, value)
        return None

    def execute_return(self, node: Return) -> Optional[Value]:
        """Execute: Return x."""
        value = None
        if node.value:
            value = self.evaluate(node.value)
        return ReturnValue(value)

    def execute_property_assignment(self, node: PropertyAssignment) -> Optional[Value]:
        """Execute: Set player.name to "Hero"."""
        obj = self.evaluate(node.object)
        value = self.evaluate(node.value)

        if obj.type != ValueType.OBJECT:
            self.error("Cannot set property on non-object", node.location)
            return None

        obj.value.set_property(node.property, value)
        return None

    def execute_index_assignment(self, node: IndexAssignment) -> Optional[Value]:
        """Execute: Set numbers at index 0 to 100."""
        obj = self.evaluate(node.object)
        index = self.evaluate(node.index)
        value = self.evaluate(node.value)

        if obj.type != ValueType.LIST:
            self.error("Cannot index non-list", node.location)
            return None

        if index.type != ValueType.NUMBER:
            self.error("Index must be a number", node.location)
            return None

        idx = index.value
        if idx < 0 or idx >= len(obj.value):
            self.error("Index out of bounds", node.location)
            return None

        obj.value[idx] = value
        return None

    def execute_list_add(self, node: ListAdd) -> Optional[Value]:
        """Execute: Add 6 to numbers."""
        list_val = self.evaluate(node.list)
        value = self.evaluate(node.value)

        if list_val.type != ValueType.LIST:
            self.error("Cannot add to non-list", node.location)
            return None

        list_val.value.append(value)
        return None

    def execute_list_remove(self, node: ListRemove) -> Optional[Value]:
        """Execute: Remove 3 from numbers."""
        list_val = self.evaluate(node.list)
        value = self.evaluate(node.value)

        if list_val.type != ValueType.LIST:
            self.error("Cannot remove from non-list", node.location)
            return None

        try:
            list_val.value.remove(value)
        except ValueError:
            self.error("Value not in list", node.location)
            return None

        return None

    def execute_file_read(self, node: FileRead) -> Optional[Value]:
        """Execute: Read the file "data.txt" into contents."""
        path = self._value_to_string(self.evaluate(node.path))

        try:
            with open(path, "r") as f:
                contents = f.read()
            self.environment.define(node.variable, create_text(contents))
        except IOError as e:
            self.error(f"Cannot read file: {e}", node.location)
            return None

        return None

    def execute_file_write(self, node: FileWrite) -> Optional[Value]:
        """Execute: Write contents to the file "output.txt"."""
        value = self._value_to_string(self.evaluate(node.value))
        path = self._value_to_string(self.evaluate(node.path))

        try:
            with open(path, "w") as f:
                f.write(value)
        except IOError as e:
            self.error(f"Cannot write file: {e}", node.location)
            return None

        return None

    def execute_file_append(self, node: FileAppend) -> Optional[Value]:
        """Execute: Append "Hello" to the file "log.txt"."""
        value = self._value_to_string(self.evaluate(node.value))
        path = self._value_to_string(self.evaluate(node.path))

        try:
            with open(path, "a") as f:
                f.write(value)
        except IOError as e:
            self.error(f"Cannot append to file: {e}", node.location)
            return None

        return None

    def execute_file_exists(self, node: FileExists) -> Optional[Value]:
        """Execute: If the file "data.txt" exists: ..."""
        path = self._value_to_string(self.evaluate(node.path))
        exists = Path(path).exists()
        return create_boolean(exists)

    def execute_directory_create(self, node: DirectoryCreate) -> Optional[Value]:
        """Execute: Create the directory "data"."""
        path = self._value_to_string(self.evaluate(node.path))

        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except IOError as e:
            self.error(f"Cannot create directory: {e}", node.location)
            return None

        return None

    def execute_directory_list(self, node: DirectoryList) -> Optional[Value]:
        """Execute: List the files in the directory "data" and store them in files."""
        path = self._value_to_string(self.evaluate(node.path))

        try:
            dir_path = Path(path)
            files = [str(f) for f in dir_path.iterdir()] if dir_path.exists() else []
            list_value = create_list([create_text(f) for f in files])
            self.environment.define(node.variable, list_value)
        except IOError as e:
            self.error(f"Cannot list directory: {e}", node.location)
            return None

        return None

    def execute_file_delete(self, node: FileDelete) -> Optional[Value]:
        """Execute: Delete the file "old.txt"."""
        path = self._value_to_string(self.evaluate(node.path))

        try:
            Path(path).unlink()
        except IOError as e:
            self.error(f"Cannot delete file: {e}", node.location)
            return None

        return None

    def execute_env_get(self, node: EnvGet) -> Optional[Value]:
        """Execute: Get the environment variable "HOME" and store it in home."""
        import os
        name = self._value_to_string(self.evaluate(node.name))
        value = os.environ.get(name, "")
        self.environment.define(node.variable, create_text(value))
        return None

    def execute_env_set(self, node: EnvSet) -> Optional[Value]:
        """Execute: Set the environment variable "MODE" to "production"."""
        import os
        name = self._value_to_string(self.evaluate(node.name))
        value = self._value_to_string(self.evaluate(node.value))
        os.environ[name] = value
        return None

    def execute_command_run(self, node: CommandRun) -> Optional[Value]:
        """Execute: Run the command "git" with arguments "status" and store the result in result."""
        import subprocess

        command = self._value_to_string(self.evaluate(node.command))
        args = [self._value_to_string(arg) for arg in node.arguments]

        try:
            result = subprocess.run([command] + args, capture_output=True, text=True)

            result_obj = create_map({
                "output": create_text(result.stdout),
                "error": create_text(result.stderr),
                "exit_code": create_number(result.returncode),
                "succeeded": create_boolean(result.returncode == 0),
            })

            self.environment.define(node.variable, result_obj)
        except Exception as e:
            self.error(f"Cannot run command: {e}", node.location)
            return None

        return None

    def execute_shell_run(self, node: ShellRun) -> Optional[Value]:
        """Execute: Run the shell command "echo hello" and store the result in result."""
        import subprocess

        command = self._value_to_string(self.evaluate(node.command))

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            result_obj = create_map({
                "output": create_text(result.stdout),
                "error": create_text(result.stderr),
                "exit_code": create_number(result.returncode),
                "succeeded": create_boolean(result.returncode == 0),
            })

            self.environment.define(node.variable, result_obj)
        except Exception as e:
            self.error(f"Cannot run shell command: {e}", node.location)
            return None

        return None

    def execute_http_request(self, node: HttpRequest) -> Optional[Value]:
        """Execute: Send a GET request to "https://example.com" and store the response in response."""
        try:
            import httpx
        except ImportError:
            self.error("httpx is required for HTTP requests", node.location)
            return None

        url = self._value_to_string(self.evaluate(node.url))
        method = node.method.lower()

        headers = {}
        if node.headers:
            headers_val = self.evaluate(node.headers)
            if headers_val.type == ValueType.MAP:
                for key, val in headers_val.value.items():
                    headers[key] = self._value_to_string(val)

        body = None
        if node.body:
            body_val = self.evaluate(node.body)
            if body_val.type == ValueType.MAP:
                body = json.loads(self._value_to_string(body_val))
            else:
                body = self._value_to_string(body_val)

        try:
            with httpx.Client() as client:
                response = client.request(method, url, headers=headers, json=body, timeout=30.0)

                response_obj = create_map({
                    "status": create_number(response.status_code),
                    "headers": create_text(str(response.headers)),
                    "body": create_text(response.text),
                    "url": create_text(str(response.url)),
                })

                self.environment.define(node.variable, response_obj)
        except Exception as e:
            self.error(f"HTTP request failed: {e}", node.location)
            return None

        return None

    def execute_json_parse(self, node: JsonParse) -> Optional[Value]:
        """Execute: Parse response.body as JSON and store it in data."""
        value = self._value_to_string(self.evaluate(node.value))

        try:
            data = json.loads(value)
            converted = self._python_to_engli(data)
            self.environment.define(node.variable, converted)
        except json.JSONDecodeError as e:
            self.error(f"Cannot parse JSON: {e}", node.location)
            return None

        return None

    def execute_json_stringify(self, node: JsonStringify) -> Optional[Value]:
        """Execute: Convert data to JSON and store it in json."""
        value = self.evaluate(node.value)
        python_value = self._engli_to_python(value)

        try:
            json_str = json.dumps(python_value)
            self.environment.define(node.variable, create_text(json_str))
        except Exception as e:
            self.error(f"Cannot stringify to JSON: {e}", node.location)
            return None

        return None

    def execute_time_now(self, node: TimeNow) -> Optional[Value]:
        """Execute: Set now to the current date and time."""
        from datetime import datetime
        now = datetime.now()
        now_str = now.isoformat()
        self.environment.define(node.variable, create_text(now_str))
        return None

    def execute_time_timestamp(self, node: TimeTimestamp) -> Optional[Value]:
        """Execute: Set timestamp to the current Unix timestamp."""
        import time
        timestamp = int(time.time())
        self.environment.define(node.variable, create_number(timestamp))
        return None

    def execute_time_sleep(self, node: TimeSleep) -> Optional[Value]:
        """Execute: Wait for 2 seconds."""
        import time
        duration = self.evaluate(node.duration)

        if duration.type == ValueType.NUMBER:
            time.sleep(duration.value)
        elif duration.type == ValueType.DECIMAL:
            time.sleep(duration.value)
        else:
            self.error("Sleep duration must be a number", node.location)
            return None

        return None

    def execute_random_number(self, node: RandomNumber) -> Optional[Value]:
        """Execute: Set number to a random number between 1 and 100."""
        import random

        min_val = self.evaluate(node.min)
        max_val = self.evaluate(node.max)

        if min_val.type != ValueType.NUMBER or max_val.type != ValueType.NUMBER:
            self.error("Random bounds must be numbers", node.location)
            return None

        result = random.randint(min_val.value, max_val.value)
        self.environment.define(node.variable, create_number(result))
        return None

    def execute_object_literal(self, node: ObjectLiteral) -> Optional[Value]:
        """Execute: Create an object called player."""
        obj = EngliObject(node.name, {})
        self.environment.define(node.name, Value(ValueType.OBJECT, obj))
        return None

    def execute_call(self, node: Call) -> Optional[Value]:
        """Execute a function call as a statement."""
        self.evaluate_call(node)
        return None



    def evaluate_identifier(self, node: Identifier) -> Value:
        """Evaluate an identifier."""
        value = self.environment.get(node.name)
        if value is None:
            self.error(f"Undefined variable: {node.name}", node.location)
            return create_error(f"Undefined variable: {node.name}")
        return value

    def evaluate_binary_operation(self, node: BinaryOperation) -> Value:
        """Evaluate a binary operation."""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        op = node.operator

        # Arithmetic
        if op == "plus":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_number(left.value + right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_decimal(float(left.value) + float(right.value))
            if left.type == ValueType.TEXT and right.type == ValueType.TEXT:
                return create_text(left.value + right.value)
            return create_error("Cannot add these types")

        if op == "minus":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_number(left.value - right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_decimal(float(left.value) - float(right.value))
            return create_error("Cannot subtract these types")

        if op == "multiplied by":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_number(left.value * right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_decimal(float(left.value) * float(right.value))
            return create_error("Cannot multiply these types")

        if op == "divided by":
            if right.type == ValueType.NUMBER and right.value == 0:
                return create_error("Division by zero")
            if right.type == ValueType.DECIMAL and right.value == 0:
                return create_error("Division by zero")
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_number(left.value // right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_decimal(float(left.value) / float(right.value))
            return create_error("Cannot divide these types")

        if op == "modulo":
            if right.type == ValueType.NUMBER and right.value == 0:
                return create_error("Modulo by zero")
            if right.type == ValueType.DECIMAL and right.value == 0:
                return create_error("Modulo by zero")
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_number(left.value % right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_decimal(float(left.value) % float(right.value))
            return create_error("Cannot modulo these types")

        # Comparisons
        if op == "is equal to":
            return create_boolean(self._values_equal(left, right))

        if op == "is not equal to":
            return create_boolean(not self._values_equal(left, right))

        if op == "is greater than":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_boolean(left.value > right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_boolean(float(left.value) > float(right.value))
            return create_error("Cannot compare these types")

        if op == "is less than":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_boolean(left.value < right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_boolean(float(left.value) < float(right.value))
            return create_error("Cannot compare these types")

        if op == "is greater than or equal to":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_boolean(left.value >= right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_boolean(float(left.value) >= float(right.value))
            return create_error("Cannot compare these types")

        if op == "is less than or equal to":
            if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
                return create_boolean(left.value <= right.value)
            if left.type == ValueType.DECIMAL or right.type == ValueType.DECIMAL:
                return create_boolean(float(left.value) <= float(right.value))
            return create_error("Cannot compare these types")

        # Boolean
        if op == "and":
            return create_boolean(left.is_truthy() and right.is_truthy())

        if op == "or":
            return create_boolean(left.is_truthy() or right.is_truthy())

        return create_error(f"Unknown operator: {op}")

    def evaluate_unary_operation(self, node: UnaryOperation) -> Value:
        """Evaluate a unary operation."""
        operand = self.evaluate(node.operand)

        if node.operator == "not":
            return create_boolean(not operand.is_truthy())

        return create_error(f"Unknown unary operator: {node.operator}")

    def evaluate_call(self, node: Call) -> Value:
        """Evaluate a function call."""
        func_value = self.evaluate(node.function)

        if func_value.type != ValueType.FUNCTION:
            return create_error("Cannot call non-function")

        func = func_value.value
        arguments = [self.evaluate(arg) for arg in node.arguments]

        if isinstance(func, EngliFunction):
            # Save current environment before calling function
            previous_env = self.environment
            result = func.call(arguments)
            # Restore environment after function call
            self.environment = previous_env
            return result
        elif isinstance(func, BuiltinFunction):
            return func.call(arguments)
        else:
            return create_error("Invalid function type")

    def evaluate_property_access(self, node: PropertyAccess) -> Value:
        """Evaluate property access: player.name."""
        obj = self.evaluate(node.object)

        if obj.type != ValueType.OBJECT:
            return create_error("Cannot access property on non-object")

        value = obj.value.get_property(node.property)
        if value is None:
            return create_error(f"Property not found: {node.property}")

        return value

    def evaluate_index_access(self, node: IndexAccess) -> Value:
        """Evaluate index access: numbers at index 0."""
        obj = self.evaluate(node.object)
        index = self.evaluate(node.index)

        if obj.type != ValueType.LIST:
            return create_error("Cannot index non-list")

        if index.type != ValueType.NUMBER:
            return create_error("Index must be a number")

        idx = index.value
        if idx < 0 or idx >= len(obj.value):
            return create_error("Index out of bounds")

        return obj.value[idx]

    def evaluate_list_literal(self, node: ListLiteral) -> Value:
        """Evaluate a list literal."""
        elements = [self.evaluate(elem) for elem in node.elements]
        return create_list(elements)

    def evaluate_map_literal(self, node: MapLiteral) -> Value:
        """Evaluate a map literal."""
        pairs = {}
        for key, value in node.pairs:
            key_str = self._value_to_string(self.evaluate(key))
            pairs[key_str] = self.evaluate(value)
        return create_map(pairs)

    def evaluate_set_literal(self, node: SetLiteral) -> Value:
        """Evaluate a set literal."""
        elements = set()
        for elem in node.elements:
            val = self.evaluate(elem)
            # Convert to hashable Python value
            if val.type == ValueType.NUMBER:
                elements.add(val.value)
            elif val.type == ValueType.TEXT:
                elements.add(val.value)
            elif val.type == ValueType.BOOLEAN:
                elements.add(val.value)
        return create_set(elements)

    def evaluate_object_literal(self, node: ObjectLiteral) -> Value:
        """Evaluate an object literal."""
        obj = EngliObject(node.name, {})
        return Value(ValueType.OBJECT, obj)

    def evaluate_type_construction(self, node: TypeConstruction) -> Value:
        """Evaluate type construction: a Player with name equal to "Hero"."""
        # Create an object with the type's fields
        obj = EngliObject(node.type_name, {})

        for field_name, field_value in node.fields:
            value = self.evaluate(field_value)
            obj.set_property(field_name, value)

        return Value(ValueType.OBJECT, obj)

    def evaluate_enum_member(self, node: EnumMember) -> Value:
        """Evaluate an enum member: Direction.North."""
        # Get the enum from environment
        enum_value = self.environment.get(node.enum_name)
        if enum_value is None or enum_value.type != ValueType.ENUM:
            return create_error(f"Unknown enum: {node.enum_name}")

        # Return the member as a text value
        return create_text(f"{node.enum_name}.{node.member}")

    def evaluate_optional(self, node: Optional) -> Value:
        """Evaluate optional: username or "Guest"."""
        value = self.evaluate(node.value)

        if value.type == ValueType.NOTHING:
            return self.evaluate(node.default)

        return value

    def evaluate_string_interpolation(self, node: StringInterpolation) -> Value:
        """Evaluate string interpolation."""
        parts = []
        for part in node.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                parts.append(self._value_to_string(self.evaluate(part)))
        return create_text("".join(parts))

    def evaluate_literal(self, node: Literal) -> Value:
        """Evaluate a literal."""
        # Handle string literals with interpolation
        if isinstance(node.value, str) and "{" in node.value:
            return self._parse_string_interpolation(node.value, node.location)

        if node.value is None:
            return create_nothing()
        if isinstance(node.value, bool):
            return create_boolean(node.value)
        if isinstance(node.value, int):
            return create_number(node.value)
        if isinstance(node.value, float):
            return create_decimal(node.value)
        if isinstance(node.value, str):
            return create_text(node.value)
        return create_error(f"Unknown literal type: {type(node.value)}")

    def _parse_string_interpolation(self, value: str, location: SourceLocation) -> Value:
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
                # Parse the expression as an identifier (simplified)
                parts.append(Identifier(NodeType.IDENTIFIER, location, expr_str.strip()))
                i = end + 1
            else:
                current += value[i]
                i += 1

        if current:
            parts.append(current)

        return self.evaluate_string_interpolation(StringInterpolation(NodeType.STRING_INTERPOLATION, location, parts))

    def _value_to_string(self, value: Value) -> str:
        """Convert a value to a string."""
        if value.type == ValueType.NOTHING:
            return ""
        if value.type == ValueType.TEXT:
            return value.value
        if value.type == ValueType.BOOLEAN:
            return "true" if value.value else "false"
        if value.type == ValueType.NUMBER:
            return str(value.value)
        if value.type == ValueType.DECIMAL:
            return str(value.value)
        if value.type == ValueType.LIST:
            return f"[{', '.join(self._value_to_string(v) for v in value.value)}]"
        if value.type == ValueType.MAP:
            pairs = [f'"{k}": {self._value_to_string(v)}' for k, v in value.value.items()]
            return f"{{{', '.join(pairs)}}}"
        return str(value.value)

    def _python_to_engli(self, value: Any) -> Value:
        """Convert a Python value to an Engli value."""
        if value is None:
            return create_nothing()
        if isinstance(value, bool):
            return create_boolean(value)
        if isinstance(value, int):
            return create_number(value)
        if isinstance(value, float):
            return create_decimal(value)
        if isinstance(value, str):
            return create_text(value)
        if isinstance(value, list):
            return create_list([self._python_to_engli(v) for v in value])
        if isinstance(value, dict):
            return create_map({k: self._python_to_engli(v) for k, v in value.items()})
        return create_error(f"Cannot convert Python type: {type(value)}")

    def _engli_to_python(self, value: Value) -> Any:
        """Convert an Engli value to a Python value."""
        if value.type == ValueType.NOTHING:
            return None
        if value.type == ValueType.BOOLEAN:
            return value.value
        if value.type == ValueType.NUMBER:
            return value.value
        if value.type == ValueType.DECIMAL:
            return value.value
        if value.type == ValueType.TEXT:
            return value.value
        if value.type == ValueType.LIST:
            return [self._engli_to_python(v) for v in value.value]
        if value.type == ValueType.MAP:
            return {k: self._engli_to_python(v) for k, v in value.value.items()}
        return None

    def error(self, message: str, location: SourceLocation) -> None:
        """Report a runtime error."""
        error = EngliRuntimeError(message, location, self.stack_trace.copy())
        raise error
