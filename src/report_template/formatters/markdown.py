"""
Markdown formatter utilities.
"""

from typing import Any, Dict


def render_markdown(template_output: str) -> str:
    """
    Process markdown output (currently a pass-through, but can add post-processing).

    Args:
        template_output: Rendered template output.

    Returns:
        Processed markdown string.
    """
    return template_output


def dict_to_markdown_table(data: Dict[str, Any], headers: tuple = ("Key", "Value")) -> str:
    """
    Convert a dictionary to a markdown table.

    Args:
        data: Dictionary to convert.
        headers: Column headers for the table.

    Returns:
        Markdown table string.
    """
    if not data:
        return ""

    lines = [
        f"| {headers[0]} | {headers[1]} |",
        f"|{'-' * (len(headers[0]) + 2)}|{'-' * (len(headers[1]) + 2)}|",
    ]

    for key, value in data.items():
        lines.append(f"| {key} | {value} |")

    return "\n".join(lines)
