"""Tests for report generator."""

import tempfile from datetime import date
from pathlib import Path

import pytest

from report_template.generator import ReportGenerator
from report_template.models import (
    FeatureDevReport,
    OutputFormat,
    Priority,
    ReportType,
    Status,
    Task,
    TeamMember,
)


@pytest.fixture
def sample_report():
    """Create a sample report for testing."""
    return FeatureDevReport(
        title="Test Report",
        project_name="Test Project",
        author="Test Author",
        feature_name="Test Feature",
        summary="This is a test summary",
        team_members=[
            TeamMember(name="John Doe", role="Developer", email="john@example.com"),
            TeamMember(name="Jane Smith", role="Designer"),
        ],
        objectives=["Objective 1", "Objective 2"],
        tasks=[
            Task(
                title="Task 1",
                status=Status.COMPLETED,
                priority=Priority.HIGH,
                assignee="John Doe"
            ),
            Task(
                title="Task 2",
                status=Status.IN_PROGRESS,
                priority=Priority.MEDIUM
            ),
        ],
        technical_approach="Using modern technologies",
    )


@pytest.fixture
def generator():
    """Create a ReportGenerator instance."""
    return ReportGenerator()


def test_generator_initialization():
    """Test ReportGenerator initialization."""
    gen = ReportGenerator()
    assert gen.templates_dir is not None
    assert gen.env is not None


def test_generate_markdown(generator, sample_report):
    """Test generating a markdown report."""
    result = generator.generate(
        sample_report,
        ReportType.FEATURE_DEV,
        OutputFormat.MARKDOWN
    )

    assert isinstance(result, str)
    assert "Test Report" in result
    assert "Test Feature" in result
    assert "Test Author" in result
    assert "John Doe" in result
    assert "Objective 1" in result
    assert "Task 1" in result


def test_generate_html(generator, sample_report):
    """Test generating an HTML report."""
    result = generator.generate(
        sample_report,
        ReportType.FEATURE_DEV,
        OutputFormat.HTML
    )

    assert isinstance(result, str)
    assert "<!DOCTYPE html>" in result
    assert "Test Report" in result
    assert "<table>" in result or "<h1>" in result


def test_generate_from_dict(generator):
    """Test generating a report from a dictionary."""
    data_dict = {
        "title": "Dict Report",
        "project_name": "Dict Project",
        "author": "Dict Author",
        "feature_name": "Dict Feature",
        "summary": "From dictionary",
    }

    result = generator.generate(
        data_dict,
        ReportType.FEATURE_DEV,
        OutputFormat.MARKDOWN
    )

    assert "Dict Report" in result
    assert "Dict Feature" in result


def test_generate_to_file_markdown(generator, sample_report):
    """Test generating a report to a markdown file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.md"

        result_path = generator.generate_to_file(
            sample_report,
            ReportType.FEATURE_DEV,
            output_path
        )

        assert result_path.exists()
        assert result_path == output_path

        content = result_path.read_text()
        assert "Test Report" in content
        assert "Test Feature" in content


def test_generate_to_file_html(generator, sample_report):
    """Test generating a report to an HTML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.html"

        result_path = generator.generate_to_file(
            sample_report,
            ReportType.FEATURE_DEV,
            output_path
        )

        assert result_path.exists()
        content = result_path.read_text()
        assert "<!DOCTYPE html>" in content or "<html" in content


def test_format_auto_detection(generator, sample_report):
    """Test automatic format detection from file extension."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test .md extension
        md_path = Path(tmpdir) / "report.md"
        generator.generate_to_file(sample_report, ReportType.FEATURE_DEV, md_path)
        assert md_path.exists()

        # Test .html extension
        html_path = Path(tmpdir) / "report.html"
        generator.generate_to_file(sample_report, ReportType.FEATURE_DEV, html_path)
        assert html_path.exists()


def test_custom_filters():
    """Test adding custom Jinja2 filters."""
    def custom_upper(value):
        return str(value).upper()

    gen = ReportGenerator(custom_filters={'custom_upper': custom_upper})
    assert 'custom_upper' in gen.env.filters


def test_list_templates(generator):
    """Test listing available templates."""
    templates = generator.list_templates()

    assert isinstance(templates, dict)
    assert ReportType.FEATURE_DEV.value in templates
    assert ReportType.PROGRAM_MGMT.value in templates
    assert ReportType.ENGINEERING_INIT.value in templates


def test_template_rendering_with_empty_lists(generator):
    """Test template rendering handles empty lists gracefully."""
    minimal_report = FeatureDevReport(
        title="Minimal",
        project_name="Project",
        author="Author",
        feature_name="Feature",
        summary="Summary"
    )

    result = generator.generate(
        minimal_report,
        ReportType.FEATURE_DEV,
        OutputFormat.MARKDOWN
    )

    assert "Minimal" in result
    # Should handle empty lists without errors


def test_date_filter(generator, sample_report):
    """Test date filter in templates."""
    result = generator.generate(
        sample_report,
        ReportType.FEATURE_DEV,
        OutputFormat.MARKDOWN
    )

    # Should contain a formatted date
    today = date.today().strftime("%Y-%m-%d")
    assert today in result or str(date.today().year) in result


def test_generate_with_custom_template_name(generator, sample_report):
    """Test generating with a custom template name."""
    # This should work with existing templates
    result = generator.generate(
        sample_report,
        ReportType.FEATURE_DEV,
        OutputFormat.MARKDOWN,
        template_name="feature_dev.md.j2"
    )

    assert "Test Report" in result
