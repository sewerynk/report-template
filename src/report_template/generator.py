"""
Core report generator using Jinja2 templates.
"""

import importlib.resources
from pathlib import Path
from typing import Any, Dict, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template

from report_template.models import (
    EngineeringInitReport,
    FeatureDevReport,
    OutputFormat,
    ProgramMgmtReport,
    ReportData,
    ReportType,
)


class ReportGenerator:
    """
    Main class for generating reports from templates.

    This class handles loading templates, rendering them with data,
    and producing output in various formats.
    """

    def __init__(self, templates_dir: Optional[Path] = None, custom_filters: Optional[Dict] = None):
        """
        Initialize the report generator.

        Args:
            templates_dir: Optional custom templates directory. If None, uses built-in templates.
            custom_filters: Optional dictionary of custom Jinja2 filters.
        """
        if templates_dir is None:
            # Use built-in templates
            templates_dir = Path(__file__).parent / "templates"
        else:
            templates_dir = Path(templates_dir)

        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        # Add custom filters
        self._setup_filters(custom_filters or {})

    def _setup_filters(self, custom_filters: Dict) -> None:
        """Set up Jinja2 filters."""
        # Default filters
        self.env.filters["date"] = lambda d: d.strftime("%Y-%m-%d") if d else "N/A"
        self.env.filters["percentage"] = lambda p: f"{p}%"

        # Add custom filters
        for name, func in custom_filters.items():
            self.env.filters[name] = func

    def _get_template_name(self, report_type: ReportType, output_format: OutputFormat) -> str:
        """Get the template filename for a report type and format."""
        format_ext = {
            OutputFormat.MARKDOWN: "md",
            OutputFormat.HTML: "html",
            OutputFormat.PDF: "html",  # PDF uses HTML template + conversion
        }

        ext = format_ext[output_format]
        return f"{report_type.value}.{ext}.j2"

    def generate(
        self,
        report_data: Union[ReportData, Dict[str, Any]],
        report_type: ReportType,
        output_format: OutputFormat = OutputFormat.MARKDOWN,
        template_name: Optional[str] = None,
    ) -> str:
        """
        Generate a report from data.

        Args:
            report_data: Report data as a Pydantic model or dictionary.
            report_type: Type of report to generate.
            output_format: Desired output format.
            template_name: Optional custom template name. If None, uses default for report_type.

        Returns:
            Rendered report as a string.
        """
        # Convert Pydantic model to dict if needed
        if isinstance(report_data, ReportData):
            data_dict = report_data.model_dump(mode="python")
        else:
            data_dict = report_data

        # Load template
        if template_name is None:
            template_name = self._get_template_name(report_type, output_format)

        template = self.env.get_template(template_name)

        # Render
        rendered = template.render(**data_dict)

        # Post-process for PDF if needed
        if output_format == OutputFormat.PDF:
            from report_template.formatters.pdf import html_to_pdf

            return html_to_pdf(rendered)

        return rendered

    def generate_to_file(
        self,
        report_data: Union[ReportData, Dict[str, Any]],
        report_type: ReportType,
        output_path: Union[str, Path],
        output_format: Optional[OutputFormat] = None,
        template_name: Optional[str] = None,
    ) -> Path:
        """
        Generate a report and save it to a file.

        Args:
            report_data: Report data as a Pydantic model or dictionary.
            report_type: Type of report to generate.
            output_path: Path where the report should be saved.
            output_format: Desired output format. If None, inferred from output_path extension.
            template_name: Optional custom template name.

        Returns:
            Path to the generated file.
        """
        output_path = Path(output_path)

        # Infer format from extension if not provided
        if output_format is None:
            ext_to_format = {
                ".md": OutputFormat.MARKDOWN,
                ".markdown": OutputFormat.MARKDOWN,
                ".html": OutputFormat.HTML,
                ".pdf": OutputFormat.PDF,
            }
            output_format = ext_to_format.get(
                output_path.suffix.lower(), OutputFormat.MARKDOWN
            )

        # Generate report
        content = self.generate(report_data, report_type, output_format, template_name)

        # Write to file
        mode = "wb" if output_format == OutputFormat.PDF else "w"
        with open(output_path, mode) as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                f.write(content)

        return output_path

    def list_templates(self) -> Dict[str, list]:
        """List available templates by report type."""
        templates = {}
        for report_type in ReportType:
            templates[report_type.value] = []
            for output_format in OutputFormat:
                template_name = self._get_template_name(report_type, output_format)
                template_path = self.templates_dir / template_name
                if template_path.exists():
                    templates[report_type.value].append(template_name)

        return templates
