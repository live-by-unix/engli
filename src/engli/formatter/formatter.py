"""
Formatter for Engli source code.
"""

import re
from typing import List


class Formatter:
    """Formats Engli source code."""

    def __init__(self, source: str):
        self.source = source
        self.lines = source.split("\n")

    def format(self) -> str:
        """Format the source code."""
        formatted_lines = []

        for line in self.lines:
            formatted = self._format_line(line)
            if formatted is not None:
                formatted_lines.append(formatted)

        return "\n".join(formatted_lines)

    def _format_line(self, line: str) -> Optional[str]:
        """Format a single line."""
        # Strip leading/trailing whitespace
        line = line.strip()

        # Skip empty lines
        if not line:
            return None

        # Ensure statements end with period
        if not line.endswith(".") and not line.endswith(":") and not line.startswith("#"):
            line += "."

        # Normalize spacing around operators
        line = self._normalize_spacing(line)

        return line

    def _normalize_spacing(self, line: str) -> str:
        """Normalize spacing in a line."""
        # Add spaces around common operators
        line = re.sub(r"\s*=\s*", " = ", line)
        line = re.sub(r"\s*\+\s*", " + ", line)
        line = re.sub(r"\s*-\s*", " - ", line)
        line = re.sub(r"\s*\*\s*", " * ", line)
        line = re.sub(r"\s*/\s*", " / ", line)

        # Clean up multiple spaces
        line = re.sub(r" +", " ", line)

        return line
