"""
Error reporting and diagnostics for Engli.
"""

from dataclasses import dataclass
from typing import List, Optional
from ..lexer.tokens import SourceLocation


@dataclass
class Diagnostic:
    """A diagnostic message (error, warning, etc.)."""

    level: str  # "error", "warning", "info"
    message: str
    location: SourceLocation
    suggestion: Optional[str] = None


class DiagnosticReporter:
    """Reports diagnostics to the user."""

    def __init__(self):
        self.diagnostics: List[Diagnostic] = []

    def add_error(self, message: str, location: SourceLocation, suggestion: Optional[str] = None) -> None:
        """Add an error diagnostic."""
        self.diagnostics.append(Diagnostic("error", message, location, suggestion))

    def add_warning(self, message: str, location: SourceLocation, suggestion: Optional[str] = None) -> None:
        """Add a warning diagnostic."""
        self.diagnostics.append(Diagnostic("warning", message, location, suggestion))

    def add_info(self, message: str, location: SourceLocation, suggestion: Optional[str] = None) -> None:
        """Add an info diagnostic."""
        self.diagnostics.append(Diagnostic("info", message, location, suggestion))

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return any(d.level == "error" for d in self.diagnostics)

    def format_diagnostic(self, diagnostic: Diagnostic) -> str:
        """Format a diagnostic for display."""
        lines = []

        # Header
        lines.append(f"{diagnostic.level}: {diagnostic.message}")

        # Location
        lines.append(f" --> {diagnostic.location}")

        # Source excerpt
        source_lines = diagnostic.location.source.split("\n")
        if 0 <= diagnostic.location.line - 1 < len(source_lines):
            line_num = diagnostic.location.line
            line_content = source_lines[line_num - 1]

            lines.append(f"  |")
            lines.append(f"{line_num} | {line_content}")
            lines.append(f"  | {' ' * (diagnostic.location.column - 1)}^")

        # Suggestion
        if diagnostic.suggestion:
            lines.append("")
            lines.append(f"  Suggestion: {diagnostic.suggestion}")

        return "\n".join(lines)

    def format_all(self) -> str:
        """Format all diagnostics."""
        if not self.diagnostics:
            return ""

        output = []
        for diagnostic in self.diagnostics:
            output.append(self.format_diagnostic(diagnostic))
            output.append("")

        return "\n".join(output)

    def clear(self) -> None:
        """Clear all diagnostics."""
        self.diagnostics.clear()
