"""
Semantic analyzer for Engli.
"""

from typing import List, Optional, Set
from dataclasses import dataclass

from ..ast import *
from ..lexer.tokens import SourceLocation
from ..diagnostics import DiagnosticReporter


@dataclass
class SemanticError:
    """A semantic analysis error."""

    message: str
    location: SourceLocation


class SemanticAnalyzer:
    """Performs semantic analysis on Engli AST."""

    def __init__(self):
        self.reporter = DiagnosticReporter()
        self.current_function: Optional[str] = None
        self.current_loop_depth = 0
        self.defined_symbols: Set[str] = set()
        self.exported_symbols: Set[str] = set()

    def analyze(self, program: Program) -> bool:
        """Analyze a program and return True if no errors."""
        self._analyze_program(program)
        return not self.reporter.has_errors()

    def _analyze_program(self, program: Program) -> None:
        """Analyze a program."""
        for stmt in program.statements:
            self._analyze_statement(stmt)

    def _analyze_statement(self, stmt: ASTNode) -> None:
        """Analyze a statement."""
        if isinstance(stmt, VariableDeclaration):
            self._analyze_variable_declaration(stmt)
        elif isinstance(stmt, VariableAssignment):
            self._analyze_variable_assignment(stmt)
        elif isinstance(stmt, ConstantDeclaration):
            self._analyze_constant_declaration(stmt)
        elif isinstance(stmt, FunctionDeclaration):
            self._analyze_function_declaration(stmt)
        elif isinstance(stmt, TypeDeclaration):
            self._analyze_type_declaration(stmt)
        elif isinstance(stmt, EnumDeclaration):
            self._analyze_enum_declaration(stmt)
        elif isinstance(stmt, Export):
            self._analyze_export(stmt)
        elif isinstance(stmt, Import):
            self._analyze_import(stmt)
        elif isinstance(stmt, IfStatement):
            self._analyze_if_statement(stmt)
        elif isinstance(stmt, WhileLoop):
            self._analyze_while_loop(stmt)
        elif isinstance(stmt, ForLoop):
            self._analyze_for_loop(stmt)
        elif isinstance(stmt, ForRangeLoop):
            self._analyze_for_range_loop(stmt)
        elif isinstance(stmt, RepeatLoop):
            self._analyze_repeat_loop(stmt)
        elif isinstance(stmt, ForeverLoop):
            self._analyze_forever_loop(stmt)
        elif isinstance(stmt, Break):
            self._analyze_break(stmt)
        elif isinstance(stmt, Continue):
            self._analyze_continue(stmt)
        elif isinstance(stmt, Return):
            self._analyze_return(stmt)
        elif isinstance(stmt, MatchStatement):
            self._analyze_match_statement(stmt)
        elif isinstance(stmt, TryStatement):
            self._analyze_try_statement(stmt)
        elif isinstance(stmt, Say):
            self._analyze_say(stmt)
        elif isinstance(stmt, Ask):
            self._analyze_ask(stmt)
        else:
            # For other statements, just analyze expressions
            self._analyze_node(stmt)

    def _analyze_node(self, node: ASTNode) -> None:
        """Analyze an AST node."""
        if isinstance(node, BinaryOperation):
            self._analyze_binary_operation(node)
        elif isinstance(node, UnaryOperation):
            self._analyze_unary_operation(node)
        elif isinstance(node, Call):
            self._analyze_call(node)
        elif isinstance(node, Identifier):
            self._analyze_identifier(node)
        elif isinstance(node, PropertyAccess):
            self._analyze_property_access(node)
        elif isinstance(node, IndexAccess):
            self._analyze_index_access(node)
        elif isinstance(node, ListLiteral):
            self._analyze_list_literal(node)
        elif isinstance(node, MapLiteral):
            self._analyze_map_literal(node)
        elif isinstance(node, SetLiteral):
            self._analyze_set_literal(node)
        elif isinstance(node, ObjectLiteral):
            self._analyze_object_literal(node)
        elif isinstance(node, TypeConstruction):
            self._analyze_type_construction(node)
        elif isinstance(node, EnumMember):
            self._analyze_enum_member(node)
        elif isinstance(node, StringInterpolation):
            self._analyze_string_interpolation(node)
        elif isinstance(node, Literal):
            pass  # Literals need no analysis
        else:
            # Recursively analyze compound nodes
            for attr_name in dir(node):
                attr = getattr(node, attr_name)
                if isinstance(attr, ASTNode):
                    self._analyze_node(attr)
                elif isinstance(attr, list):
                    for item in attr:
                        if isinstance(item, ASTNode):
                            self._analyze_node(item)
                        elif isinstance(item, tuple):
                            for tuple_item in item:
                                if isinstance(tuple_item, ASTNode):
                                    self._analyze_node(tuple_item)

    def _analyze_variable_declaration(self, stmt: VariableDeclaration) -> None:
        """Analyze a variable declaration."""
        self.defined_symbols.add(stmt.name)
        self._analyze_node(stmt.value)

    def _analyze_variable_assignment(self, stmt: VariableAssignment) -> None:
        """Analyze a variable assignment."""
        if stmt.name not in self.defined_symbols:
            self.reporter.add_error(
                f"Assignment to undefined variable: {stmt.name}",
                stmt.location,
                "Declare the variable before assigning to it"
            )
        self._analyze_node(stmt.value)

    def _analyze_constant_declaration(self, stmt: ConstantDeclaration) -> None:
        """Analyze a constant declaration."""
        self.defined_symbols.add(stmt.name)
        self._analyze_node(stmt.value)

    def _analyze_function_declaration(self, stmt: FunctionDeclaration) -> None:
        """Analyze a function declaration."""
        self.defined_symbols.add(stmt.name)

        # Save current function context
        old_function = self.current_function
        self.current_function = stmt.name

        # Analyze function body
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)

        # Restore function context
        self.current_function = old_function

    def _analyze_type_declaration(self, stmt: TypeDeclaration) -> None:
        """Analyze a type declaration."""
        self.defined_symbols.add(stmt.name)

    def _analyze_enum_declaration(self, stmt: EnumDeclaration) -> None:
        """Analyze an enum declaration."""
        self.defined_symbols.add(stmt.name)

    def _analyze_export(self, stmt: Export) -> None:
        """Analyze an export statement."""
        if stmt.name not in self.defined_symbols:
            self.reporter.add_error(
                f"Export of undefined symbol: {stmt.name}",
                stmt.location,
                "Define the symbol before exporting it"
            )
        self.exported_symbols.add(stmt.name)

    def _analyze_import(self, stmt: Import) -> None:
        """Analyze an import statement."""
        # For now, we just note the import
        # In a full implementation, we would check the imported file
        pass

    def _analyze_if_statement(self, stmt: IfStatement) -> None:
        """Analyze an if statement."""
        self._analyze_node(stmt.condition)

        for body_stmt in stmt.then_block:
            self._analyze_statement(body_stmt)

        for elif_condition, elif_block in stmt.elif_blocks:
            self._analyze_node(elif_condition)
            for body_stmt in elif_block:
                self._analyze_statement(body_stmt)

        if stmt.else_block:
            for body_stmt in stmt.else_block:
                self._analyze_statement(body_stmt)

    def _analyze_while_loop(self, stmt: WhileLoop) -> None:
        """Analyze a while loop."""
        self.current_loop_depth += 1
        self._analyze_node(stmt.condition)
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.current_loop_depth -= 1

    def _analyze_for_loop(self, stmt: ForLoop) -> None:
        """Analyze a for loop."""
        self.current_loop_depth += 1
        self.defined_symbols.add(stmt.variable)
        self._analyze_node(stmt.iterable)
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.current_loop_depth -= 1

    def _analyze_for_range_loop(self, stmt: ForRangeLoop) -> None:
        """Analyze a for range loop."""
        self.current_loop_depth += 1
        self.defined_symbols.add(stmt.variable)
        self._analyze_node(stmt.start)
        self._analyze_node(stmt.end)
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.current_loop_depth -= 1

    def _analyze_repeat_loop(self, stmt: RepeatLoop) -> None:
        """Analyze a repeat loop."""
        self.current_loop_depth += 1
        self._analyze_node(stmt.count)
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.current_loop_depth -= 1

    def _analyze_forever_loop(self, stmt: ForeverLoop) -> None:
        """Analyze a forever loop."""
        self.current_loop_depth += 1
        for body_stmt in stmt.body:
            self._analyze_statement(body_stmt)
        self.current_loop_depth -= 1

    def _analyze_break(self, stmt: Break) -> None:
        """Analyze a break statement."""
        if self.current_loop_depth == 0:
            self.reporter.add_error(
                "Break outside of loop",
                stmt.location,
                "Break can only be used inside a loop"
            )

    def _analyze_continue(self, stmt: Continue) -> None:
        """Analyze a continue statement."""
        if self.current_loop_depth == 0:
            self.reporter.add_error(
                "Continue outside of loop",
                stmt.location,
                "Continue can only be used inside a loop"
            )

    def _analyze_return(self, stmt: Return) -> None:
        """Analyze a return statement."""
        if self.current_function is None:
            self.reporter.add_error(
                "Return outside of function",
                stmt.location,
                "Return can only be used inside a function"
            )
        if stmt.value:
            self._analyze_node(stmt.value)

    def _analyze_match_statement(self, stmt: MatchStatement) -> None:
        """Analyze a match statement."""
        self._analyze_node(stmt.value)

        for condition, body in stmt.cases:
            self._analyze_node(condition)
            for body_stmt in body:
                self._analyze_statement(body_stmt)

        if stmt.default_case:
            for body_stmt in stmt.default_case:
                self._analyze_statement(body_stmt)

    def _analyze_try_statement(self, stmt: TryStatement) -> None:
        """Analyze a try statement."""
        for body_stmt in stmt.try_block:
            self._analyze_statement(body_stmt)

        self.defined_symbols.add(stmt.error_name)

        for body_stmt in stmt.catch_block:
            self._analyze_statement(body_stmt)

    def _analyze_say(self, stmt: Say) -> None:
        """Analyze a say statement."""
        self._analyze_node(stmt.value)

    def _analyze_ask(self, stmt: Ask) -> None:
        """Analyze an ask statement."""
        self._analyze_node(stmt.prompt)
        self.defined_symbols.add(stmt.variable)

    def _analyze_binary_operation(self, node: BinaryOperation) -> None:
        """Analyze a binary operation."""
        self._analyze_node(node.left)
        self._analyze_node(node.right)

    def _analyze_unary_operation(self, node: UnaryOperation) -> None:
        """Analyze a unary operation."""
        self._analyze_node(node.operand)

    def _analyze_call(self, node: Call) -> None:
        """Analyze a function call."""
        self._analyze_node(node.function)
        for arg in node.arguments:
            self._analyze_node(arg)

    def _analyze_identifier(self, node: Identifier) -> None:
        """Analyze an identifier."""
        if node.name not in self.defined_symbols:
            self.reporter.add_error(
                f"Use of undefined variable: {node.name}",
                node.location,
                f"Define the variable before using it"
            )

    def _analyze_property_access(self, node: PropertyAccess) -> None:
        """Analyze property access."""
        self._analyze_node(node.object)

    def _analyze_index_access(self, node: IndexAccess) -> None:
        """Analyze index access."""
        self._analyze_node(node.object)
        self._analyze_node(node.index)

    def _analyze_list_literal(self, node: ListLiteral) -> None:
        """Analyze a list literal."""
        for elem in node.elements:
            self._analyze_node(elem)

    def _analyze_map_literal(self, node: MapLiteral) -> None:
        """Analyze a map literal."""
        for key, value in node.pairs:
            self._analyze_node(key)
            self._analyze_node(value)

    def _analyze_set_literal(self, node: SetLiteral) -> None:
        """Analyze a set literal."""
        for elem in node.elements:
            self._analyze_node(elem)

    def _analyze_object_literal(self, node: ObjectLiteral) -> None:
        """Analyze an object literal."""
        self.defined_symbols.add(node.name)

    def _analyze_type_construction(self, node: TypeConstruction) -> None:
        """Analyze type construction."""
        if node.type_name not in self.defined_symbols:
            self.reporter.add_error(
                f"Use of undefined type: {node.type_name}",
                node.location,
                f"Define the type before using it"
            )
        for field_name, field_value in node.fields:
            self._analyze_node(field_value)

    def _analyze_enum_member(self, node: EnumMember) -> None:
        """Analyze an enum member."""
        if node.enum_name not in self.defined_symbols:
            self.reporter.add_error(
                f"Use of undefined enum: {node.enum_name}",
                node.location,
                f"Define the enum before using it"
            )

    def _analyze_string_interpolation(self, node: StringInterpolation) -> None:
        """Analyze string interpolation."""
        for part in node.parts:
            if isinstance(part, ASTNode):
                self._analyze_node(part)

    def get_errors(self) -> List[SemanticError]:
        """Get all semantic errors."""
        return [SemanticError(d.message, d.location) for d in self.reporter.diagnostics if d.level == "error"]
