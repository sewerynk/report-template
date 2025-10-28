"""
Command-line interface for report generation.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
import yaml

from report_template.generator import ReportGenerator
from report_template.models import (
    EngineeringInitReport,
    FeatureDevReport,
    OutputFormat,
    ProgramMgmtReport,
    ReportType,
)


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """
    Generate standardized, professional project reports.

    This tool helps create consistent documentation for feature development,
    program management, and engineering initiatives.
    """
    pass


@main.command()
@click.argument("data_file", type=click.Path(exists=True))
@click.option(
    "-t",
    "--type",
    "report_type",
    type=click.Choice([t.value for t in ReportType]),
    required=True,
    help="Type of report to generate",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    required=True,
    help="Output file path",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice([f.value for f in OutputFormat]),
    default=None,
    help="Output format (auto-detected from file extension if not specified)",
)
@click.option(
    "--template-dir",
    type=click.Path(exists=True),
    default=None,
    help="Custom templates directory",
)
@click.option(
    "--template",
    default=None,
    help="Custom template name (overrides default)",
)
def generate(
    data_file: str,
    report_type: str,
    output: str,
    output_format: Optional[str],
    template_dir: Optional[str],
    template: Optional[str],
) -> None:
    """
    Generate a report from a data file.

    DATA_FILE: Path to YAML or JSON file containing report data

    Examples:

    \b
    # Generate a feature development report in Markdown
    report-gen generate data.yaml -t feature_dev -o report.md

    \b
    # Generate a program management report in PDF
    report-gen generate data.json -t program_mgmt -o report.pdf

    \b
    # Generate a Word document for email distribution
    report-gen generate data.yaml -t feature_dev -o report.docx

    \b
    # Use custom template (not applicable for DOCX)
    report-gen generate data.yaml -t feature_dev -o report.md --template my_template.md.j2
    """
    try:
        # Load data file
        data_path = Path(data_file)
        with open(data_path) as f:
            if data_path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif data_path.suffix == ".json":
                data = json.load(f)
            else:
                click.echo(
                    f"Error: Unsupported file format '{data_path.suffix}'. Use .yaml, .yml, or .json",
                    err=True,
                )
                sys.exit(1)

        # Validate data with appropriate model
        report_type_enum = ReportType(report_type)
        model_map = {
            ReportType.FEATURE_DEV: FeatureDevReport,
            ReportType.PROGRAM_MGMT: ProgramMgmtReport,
            ReportType.ENGINEERING_INIT: EngineeringInitReport,
        }

        model_class = model_map[report_type_enum]
        report_data = model_class(**data)

        # Initialize generator
        generator = ReportGenerator(
            templates_dir=Path(template_dir) if template_dir else None
        )

        # Convert format string to enum if provided
        format_enum = OutputFormat(output_format) if output_format else None

        # Generate report
        output_path = generator.generate_to_file(
            report_data=report_data,
            report_type=report_type_enum,
            output_path=output,
            output_format=format_enum,
            template_name=template,
        )

        click.echo(f"Report generated successfully: {output_path}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "-t",
    "--type",
    "report_type",
    type=click.Choice([t.value for t in ReportType]),
    required=True,
    help="Type of report template",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    required=True,
    help="Output file path for sample data",
)
@click.option(
    "-f",
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format for sample data",
)
def init(report_type: str, output: str, output_format: str) -> None:
    """
    Initialize a sample data file for a report type.

    This creates a template data file with example values that you can
    customize for your specific needs.

    Examples:

    \b
    # Create sample feature development data
    report-gen init -t feature_dev -o my_feature.yaml

    \b
    # Create sample program management data in JSON
    report-gen init -t program_mgmt -o my_program.json -f json
    """
    from datetime import date, timedelta

    # Sample data templates
    samples = {
        ReportType.FEATURE_DEV: {
            "title": "Feature Development Report",
            "project_name": "My Project",
            "author": "John Doe",
            "feature_name": "User Authentication",
            "repository": "https://github.com/org/repo",
            "branch": "feature/auth",
            "sprint": "Sprint 5",
            "summary": "Implementation of user authentication system with OAuth2 support.",
            "team_members": [
                {"name": "John Doe", "role": "Lead Developer", "email": "john@example.com"},
                {"name": "Jane Smith", "role": "Backend Developer", "email": "jane@example.com"},
            ],
            "objectives": [
                "Implement secure user authentication",
                "Support OAuth2 providers (Google, GitHub)",
                "Add session management",
            ],
            "requirements": [
                "Password must be at least 12 characters",
                "Support multi-factor authentication",
                "Implement rate limiting",
            ],
            "technical_approach": "Using FastAPI for backend, JWT for tokens, and Redis for session storage.",
            "tasks": [
                {
                    "title": "Design authentication flow",
                    "assignee": "John Doe",
                    "status": "Completed",
                    "priority": "High",
                    "jira_id": "AUTH-101",
                    "target_start_date": str(date.today() - timedelta(days=10)),
                    "target_end_date": str(date.today() - timedelta(days=5)),
                },
                {
                    "title": "Implement OAuth2 integration",
                    "assignee": "Jane Smith",
                    "status": "In Progress",
                    "priority": "High",
                    "jira_id": "AUTH-102",
                    "target_start_date": str(date.today() - timedelta(days=3)),
                    "target_end_date": str(date.today() + timedelta(days=4)),
                    "due_date": str(date.today() + timedelta(days=7)),
                },
            ],
            "testing_strategy": "Unit tests for auth logic, integration tests for OAuth flow, security testing.",
            "deployment_plan": "Rolling deployment to staging, then production after QA approval.",
            "risks": [
                {
                    "description": "OAuth provider downtime",
                    "impact": "High",
                    "likelihood": "Low",
                    "mitigation": "Implement fallback to local authentication",
                }
            ],
        },
        ReportType.PROGRAM_MGMT: {
            "title": "Program Management Report",
            "project_name": "Digital Transformation Initiative",
            "program_name": "Q4 2024 Platform Modernization",
            "author": "Alice Johnson",
            "reporting_period": "October 2024",
            "status": "In Progress",
            "summary": "Monthly update on platform modernization efforts.",
            "executive_summary": "The platform modernization program is on track with 3 out of 5 milestones completed.",
            "stakeholders": ["CTO", "VP Engineering", "Product Leadership"],
            "budget_summary": "75% of allocated budget utilized, on track for completion within budget.",
            "team_members": [
                {"name": "Alice Johnson", "role": "Program Manager"},
                {"name": "Bob Williams", "role": "Tech Lead"},
            ],
            "milestones": [
                {
                    "name": "Phase 1: Assessment",
                    "target_date": str(date.today() - timedelta(days=60)),
                    "status": "Completed",
                    "completion_percentage": 100,
                }
            ],
            "key_achievements": [
                "Completed infrastructure migration",
                "Onboarded 5 new team members",
            ],
            "kpis": {
                "System Uptime": "99.9%",
                "Customer Satisfaction": "4.5/5",
                "Deployment Frequency": "Daily",
            },
        },
        ReportType.ENGINEERING_INIT: {
            "title": "Engineering Initiative Report",
            "project_name": "Infrastructure Modernization",
            "initiative_name": "Kubernetes Migration",
            "initiative_type": "Infrastructure",
            "author": "Charlie Brown",
            "status": "In Progress",
            "summary": "Migration of all services from EC2 to Kubernetes for better scalability.",
            "sponsors": ["VP Engineering", "CTO"],
            "team_members": [
                {"name": "Charlie Brown", "role": "DevOps Lead"},
                {"name": "Diana Prince", "role": "SRE"},
            ],
            "start_date": str(date.today() - timedelta(days=30)),
            "target_completion_date": str(date.today() + timedelta(days=90)),
            "objectives": [
                "Migrate all production services to Kubernetes",
                "Improve deployment automation",
                "Reduce infrastructure costs by 30%",
            ],
            "scope": "Migration of 25 microservices to EKS, implementation of GitOps workflows.",
            "technical_details": "Using EKS, ArgoCD for GitOps, Prometheus for monitoring.",
            "success_criteria": [
                "All services running on Kubernetes",
                "Zero downtime during migration",
                "30% cost reduction achieved",
            ],
            "impact_analysis": "Improved scalability, faster deployments, reduced operational overhead.",
            "resources_required": "2 DevOps engineers, 1 SRE, AWS EKS clusters.",
        },
    }

    try:
        report_type_enum = ReportType(report_type)
        sample_data = samples[report_type_enum]

        output_path = Path(output)

        # Write sample data
        with open(output_path, "w") as f:
            if output_format == "yaml":
                yaml.dump(sample_data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(sample_data, f, indent=2, default=str)

        click.echo(f"Sample data file created: {output_path}")
        click.echo(f"\nEdit this file with your data, then generate a report with:")
        click.echo(f"  report-gen generate {output_path} -t {report_type} -o report.md")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--template-dir",
    type=click.Path(exists=True),
    default=None,
    help="Custom templates directory",
)
def list_templates(template_dir: Optional[str]) -> None:
    """List available templates."""
    try:
        generator = ReportGenerator(
            templates_dir=Path(template_dir) if template_dir else None
        )
        templates = generator.list_templates()

        click.echo("Available templates:\n")
        for report_type, template_list in templates.items():
            click.echo(f"{report_type}:")
            for template in template_list:
                click.echo(f"  - {template}")
            click.echo()

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
