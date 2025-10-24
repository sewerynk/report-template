"""
PDF formatter utilities using WeasyPrint.
"""

from typing import Union

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


def html_to_pdf(html_content: str) -> bytes:
    """
    Convert HTML content to PDF.

    Args:
        html_content: HTML string to convert.

    Returns:
        PDF content as bytes.

    Raises:
        ImportError: If WeasyPrint is not installed.
    """
    if not WEASYPRINT_AVAILABLE:
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it with: pip install weasyprint"
        )

    # Convert HTML to PDF
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


def markdown_to_pdf(markdown_text: str) -> bytes:
    """
    Convert markdown directly to PDF.

    Args:
        markdown_text: Markdown text to convert.

    Returns:
        PDF content as bytes.
    """
    from report_template.formatters.html import render_html

    html_content = render_html(markdown_text, include_css=True)
    return html_to_pdf(html_content)
