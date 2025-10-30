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
            "action_points": [
                {
                    "description": "Review security audit findings and implement recommendations",
                    "priority": "High",
                    "status": "In Progress",
                    "owner": "Security Team",
                    "due_date": str(date.today() + timedelta(days=7)),
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


@main.command()
@click.argument("data_file", type=click.Path(exists=True))
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=".jira.config.yaml",
    help="Path to JIRA configuration file",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output file path (updates input file if not specified)",
)
def sync_jira(data_file: str, config: str, output: Optional[str]) -> None:
    """
    Sync task data with JIRA server.

    Fetches latest data from JIRA for all tasks that have a jira_id field.
    You can create minimal tasks with ONLY jira_id, and all other fields
    will be automatically populated from JIRA!

    Workflow:
    1. Create a YAML file with minimal tasks (just jira_id)
    2. Run sync-jira to fetch all data from JIRA
    3. Generate your report with complete task information

    Examples:

    \b
    # Create a minimal YAML file:
    # tasks:
    #   - jira_id: K2A-1237
    #   - jira_id: K2A-1238
    #   - jira_id: K2A-1239

    \b
    # Sync to fetch all task data from JIRA
    report-gen sync-jira my_tasks.yaml

    \b
    # Sync and save to new file
    report-gen sync-jira feature_data.yaml -o feature_data_synced.yaml

    \b
    # Use custom config file
    report-gen sync-jira feature_data.yaml --config ~/my-jira-config.yaml
    """
    try:
        from report_template.jira_client import create_jira_client

        # Load JIRA config
        config_path = Path(config)
        if not config_path.exists():
            click.echo(
                f"Error: JIRA config file not found: {config_path}\n"
                f"Create one from: .jira.config.example.yaml",
                err=True
            )
            sys.exit(1)

        with open(config_path) as f:
            jira_config = yaml.safe_load(f).get('jira', {})

        # Create JIRA client
        try:
            jira_client = create_jira_client(jira_config)
            click.echo(f"✓ Connected to JIRA: {jira_config['url']}")
        except Exception as e:
            click.echo(f"Error connecting to JIRA: {str(e)}", err=True)
            sys.exit(1)

        # Load data file
        data_path = Path(data_file)
        with open(data_path) as f:
            if data_path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif data_path.suffix == ".json":
                data = json.load(f)
            else:
                click.echo(f"Error: Unsupported file format '{data_path.suffix}'", err=True)
                sys.exit(1)

        # Sync tasks
        tasks = data.get('tasks', [])
        if not tasks:
            click.echo("No tasks found in data file.")
            sys.exit(0)

        click.echo(f"\nSyncing {len(tasks)} tasks...")
        updated_tasks = jira_client.sync_tasks(tasks)
        data['tasks'] = updated_tasks

        # Save to output file
        output_path = Path(output) if output else data_path
        with open(output_path, 'w') as f:
            if output_path.suffix in [".yaml", ".yml"]:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(data, f, indent=2, default=str)

        click.echo(f"\n✓ Synced data saved to: {output_path}")

    except ImportError:
        click.echo(
            "Error: JIRA integration not available. "
            "Install with: pip install atlassian-python-api",
            err=True
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("jira_ids", nargs=-1, required=True)
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=".jira.config.yaml",
    help="Path to JIRA configuration file",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    required=True,
    help="Output file path for fetched tasks",
)
def fetch_tickets(jira_ids: tuple, config: str, output: str) -> None:
    """
    Fetch tasks from JIRA using ticket IDs (simpler than JQL queries).

    This is the easiest way to create a report from JIRA tickets.
    Just provide the ticket IDs and all data will be fetched automatically.

    Examples:

    \b
    # Fetch specific tickets
    report-gen fetch-tickets PROJ-123 PROJ-124 PROJ-125 -o tasks.yaml

    \b
    # Fetch tickets for your report
    report-gen fetch-tickets AUTH-101 AUTH-102 AUTH-103 -o feature_report.yaml

    \b
    # Then generate the report
    report-gen generate feature_report.yaml -t feature_dev -o report.docx
    """
    try:
        from report_template.jira_client import create_jira_client

        # Load JIRA config
        config_path = Path(config)
        if not config_path.exists():
            click.echo(
                f"Error: JIRA config file not found: {config_path}\n"
                f"Create one from: .jira.config.example.yaml",
                err=True
            )
            sys.exit(1)

        with open(config_path) as f:
            jira_config = yaml.safe_load(f).get('jira', {})

        # Create JIRA client
        try:
            jira_client = create_jira_client(jira_config)
            click.echo(f"✓ Connected to JIRA: {jira_config['url']}")
        except Exception as e:
            click.echo(f"Error connecting to JIRA: {str(e)}", err=True)
            sys.exit(1)

        # Fetch each ticket
        click.echo(f"\nFetching {len(jira_ids)} JIRA tickets...")
        tasks = []

        for jira_id in jira_ids:
            try:
                issue = jira_client.get_issue(jira_id)
                task_data = jira_client.issue_to_task_data(issue)
                tasks.append(task_data)
                click.echo(f"✓ Fetched {jira_id}: {task_data['title']}")
            except Exception as e:
                click.echo(f"✗ Failed to fetch {jira_id}: {str(e)}", err=True)

        if not tasks:
            click.echo("No tasks fetched successfully.")
            sys.exit(1)

        click.echo(f"\n✓ Successfully fetched {len(tasks)} tasks from JIRA")

        # Create minimal data structure
        data = {
            'tasks': tasks,
            'title': 'Report from JIRA',
            'project_name': 'Project',
            'author': 'Auto-generated',
            'summary': f'Tasks fetched from JIRA tickets: {", ".join(jira_ids)}'
        }

        # Save to output file
        output_path = Path(output)
        with open(output_path, 'w') as f:
            if output_path.suffix in [".yaml", ".yml"]:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(data, f, indent=2, default=str)

        click.echo(f"✓ Tasks saved to: {output_path}")
        click.echo(f"\nYou can now generate a report with:")
        click.echo(f"  report-gen generate {output_path} -t feature_dev -o report.docx")

    except ImportError:
        click.echo(
            "Error: JIRA integration not available. "
            "Install with: pip install atlassian-python-api",
            err=True
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("report_file", type=click.Path(exists=True))
@click.option(
    "--config",
    type=click.Path(exists=True),
    default="conflu.json",
    help="Path to Confluence configuration file (JSON)",
)
@click.option(
    "--title",
    type=str,
    default=None,
    help="Page title (defaults to report title from data file)",
)
@click.option(
    "--space",
    type=str,
    default=None,
    help="Confluence space key (overrides config file)",
)
@click.option(
    "--parent-id",
    type=str,
    default=None,
    help="Parent page ID (optional, for creating page under a parent)",
)
def push_confluence(
    report_file: str,
    config: str,
    title: Optional[str],
    space: Optional[str],
    parent_id: Optional[str]
) -> None:
    """
    Push a generated report to Confluence.

    This command takes an HTML report file and pushes it to a Confluence page.
    If the page already exists (matched by title), it will be updated.
    Otherwise, a new page will be created.

    The report file should be generated first using the 'generate' command
    with HTML format.

    Examples:

    \b
    # Generate HTML report first
    report-gen generate my_report.yaml -t feature_dev -o report.html

    \b
    # Push to Confluence (will create or update page)
    report-gen push-confluence report.html

    \b
    # Push with custom title
    report-gen push-confluence report.html --title "Weekly Status Report"

    \b
    # Push to specific space
    report-gen push-confluence report.html --space "MYSPACE"

    \b
    # Push under a parent page
    report-gen push-confluence report.html --parent-id "123456789"
    """
    try:
        from report_template.confluence_client import create_confluence_client

        # Load Confluence config
        config_path = Path(config)
        if not config_path.exists():
            click.echo(
                f"Error: Confluence config file not found: {config_path}\n"
                f"Create one from: conflu.json.example",
                err=True
            )
            sys.exit(1)

        with open(config_path) as f:
            confluence_config = json.load(f).get('confluence', {})

        # Create Confluence client
        try:
            confluence_client = create_confluence_client(confluence_config)
            click.echo(f"✓ Connected to Confluence: {confluence_config['url']}")
        except Exception as e:
            click.echo(f"Error connecting to Confluence: {str(e)}", err=True)
            sys.exit(1)

        # Read report file
        report_path = Path(report_file)
        if report_path.suffix not in ['.html', '.htm']:
            click.echo(
                "Error: Report file must be HTML format.\n"
                "Generate HTML report first: report-gen generate data.yaml -t feature_dev -o report.html",
                err=True
            )
            sys.exit(1)

        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Prepare HTML for Confluence storage format
        click.echo("Preparing HTML for Confluence...")
        html_content = confluence_client.prepare_html_for_confluence(html_content)

        # Determine space key
        space_key = space or confluence_config.get('space_key')
        if not space_key:
            click.echo(
                "Error: Space key not specified.\n"
                "Either set it in conflu.json or use --space option.",
                err=True
            )
            sys.exit(1)

        # Determine page title
        page_title = title or report_path.stem
        click.echo(f"Page title: {page_title}")
        click.echo(f"Space: {space_key}")

        # Determine parent ID
        page_parent_id = parent_id or confluence_config.get('parent_page_id')
        if page_parent_id:
            click.echo(f"Parent page ID: {page_parent_id}")

        # Push to Confluence
        click.echo("\nPushing to Confluence...")
        result = confluence_client.create_or_update_page(
            space_key=space_key,
            title=page_title,
            content=html_content,
            parent_id=page_parent_id
        )

        page_url = confluence_client.get_page_url(result)
        click.echo(f"\n✓ Successfully pushed to Confluence!")
        click.echo(f"  Page URL: {page_url}")

    except ImportError:
        click.echo(
            "Error: Requests library not available. "
            "Install with: pip install requests",
            err=True
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
