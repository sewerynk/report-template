"""
HTML formatter utilities.
"""

import markdown


def render_html(markdown_text: str, include_css: bool = True) -> str:
    """
    Convert markdown to HTML with optional CSS styling.

    Args:
        markdown_text: Markdown text to convert.
        include_css: Whether to include default CSS styling.

    Returns:
        HTML string.
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "codehilite", "toc"],
    )

    if not include_css:
        return html_content

    # Wrap with HTML document and CSS
    css = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        h3 {
            color: #546e7a;
            margin-top: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        li {
            margin: 5px 0;
        }
        .metadata {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .status-completed {
            color: #27ae60;
            font-weight: bold;
        }
        .status-in-progress {
            color: #f39c12;
            font-weight: bold;
        }
        .status-blocked {
            color: #e74c3c;
            font-weight: bold;
        }
        .priority-high, .priority-critical {
            color: #e74c3c;
            font-weight: bold;
        }
        .priority-medium {
            color: #f39c12;
        }
        .priority-low {
            color: #95a5a6;
        }
    </style>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report</title>
    {css}
</head>
<body>
    {html_content}
</body>
</html>
"""
