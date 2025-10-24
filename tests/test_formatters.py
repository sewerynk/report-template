"""Tests for formatters."""

import pytest

from report_template.formatters.html import render_html
from report_template.formatters.markdown import dict_to_markdown_table, render_markdown


def test_render_markdown():
    """Test markdown renderer (pass-through)."""
    text = "# Heading\n\nParagraph"
    result = render_markdown(text)
    assert result == text


def test_dict_to_markdown_table():
    """Test dictionary to markdown table conversion."""
    data = {
        "Name": "John Doe",
        "Role": "Developer",
        "Status": "Active"
    }

    result = dict_to_markdown_table(data)

    assert "| Key | Value |" in result
    assert "| Name | John Doe |" in result
    assert "| Role | Developer |" in result
    assert "| Status | Active |" in result


def test_dict_to_markdown_table_empty():
    """Test empty dictionary."""
    result = dict_to_markdown_table({})
    assert result == ""


def test_dict_to_markdown_table_custom_headers():
    """Test custom table headers."""
    data = {"metric1": "value1", "metric2": "value2"}
    result = dict_to_markdown_table(data, headers=("Metric", "Value"))

    assert "| Metric | Value |" in result


def test_render_html_without_css():
    """Test HTML rendering without CSS."""
    markdown_text = "# Heading\n\nParagraph"
    result = render_html(markdown_text, include_css=False)

    assert "<h1>Heading</h1>" in result
    assert "<p>Paragraph</p>" in result
    assert "<!DOCTYPE html>" not in result


def test_render_html_with_css():
    """Test HTML rendering with CSS."""
    markdown_text = "# Heading\n\nParagraph"
    result = render_html(markdown_text, include_css=True)

    assert "<!DOCTYPE html>" in result
    assert "<style>" in result
    assert "<h1>Heading</h1>" in result
    assert "<p>Paragraph</p>" in result


def test_render_html_table():
    """Test HTML rendering of markdown table."""
    markdown_text = """
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
"""

    result = render_html(markdown_text, include_css=False)

    assert "<table>" in result
    assert "<th>Column 1</th>" in result
    assert "<td>Value 1</td>" in result


def test_render_html_code_blocks():
    """Test HTML rendering of code blocks."""
    markdown_text = """
```python
def hello():
    print("Hello, World!")
```
"""

    result = render_html(markdown_text, include_css=False)

    assert "<code>" in result or "<pre>" in result
