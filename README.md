# report-template

A Python-based solution for generating standardized, professional project reports tailored for feature development, program management, and engineering initiatives. This template system enables consistent documentation across technical projects while maintaining flexibility for custom requirements.

## Features

- **Multiple Report Types**: Feature development, program management, and engineering initiatives
- **Flexible Output Formats**: Markdown, HTML, PDF, and Word (DOCX) support
- **JIRA Integration**: Automatically fetch and sync task data from JIRA server
- **Template-Based**: Fully customizable Jinja2 templates
- **CLI & Python API**: Use via command-line or programmatically
- **Data Validation**: Pydantic models ensure data integrity
- **Professional Styling**: Beautiful, ready-to-use templates with modern design
- **Extensible**: Easy to add custom report types and templates

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/report-template.git
cd report-template

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Generate Your First Report

```bash
# Step 1: Create a sample data file
report-gen init -t feature_dev -o my_feature.yaml

# Step 2: Edit my_feature.yaml with your project data
# (Use any text editor)

# Step 3: Generate the report
report-gen generate my_feature.yaml -t feature_dev -o my_report.md
```

That's it! Your professional report is ready at `my_report.md`.

## Report Types

### 1. Feature Development Reports

Perfect for documenting feature development efforts with technical details, tasks, and milestones.

```bash
report-gen init -t feature_dev -o feature.yaml
report-gen generate feature.yaml -t feature_dev -o feature_report.md
```

**Key Sections:**
- Team and objectives
- Technical approach & architecture
- Tasks and progress tracking
- Milestones and timeline
- Testing strategy
- Deployment plan
- Risks and dependencies

### 2. Program Management Reports

Ideal for program-level status reporting to stakeholders and executives.

```bash
report-gen init -t program_mgmt -o program.yaml
report-gen generate program.yaml -t program_mgmt -o program_report.md
```

**Key Sections:**
- Executive summary
- Stakeholders and team composition
- KPIs and metrics
- Milestones and progress
- Key achievements
- Challenges and risks
- Budget summary
- Decisions needed

### 3. Engineering Initiative Reports

For documenting major engineering initiatives like infrastructure modernization or architectural changes.

```bash
report-gen init -t engineering_init -o initiative.yaml
report-gen generate initiative.yaml -t engineering_init -o initiative_report.md
```

**Key Sections:**
- Objectives and scope
- Technical details & architecture
- Implementation phases
- Success criteria
- Impact analysis
- Resource requirements
- Rollout strategy

## Output Formats

### Markdown (Default)

Great for version control and collaboration:

```bash
report-gen generate data.yaml -t feature_dev -o report.md
```

### HTML

Professional web format with beautiful styling:

```bash
report-gen generate data.yaml -t feature_dev -o report.html
```

### PDF

Print-ready format for distribution:

```bash
# Requires WeasyPrint: pip install weasyprint
report-gen generate data.yaml -t feature_dev -o report.pdf
```

### Word Document (DOCX)

Perfect for email distribution and collaboration:

```bash
report-gen generate data.yaml -t feature_dev -o report.docx
```

The DOCX format is ideal for:
- Sending reports via email
- Sharing with stakeholders who prefer Microsoft Word
- Further editing and customization in Word
- Corporate environments requiring .docx format

## JIRA Integration

Automatically fetch task data from your JIRA server!

### Quick Start with JIRA

```bash
# 1. Setup JIRA configuration (one-time setup)
cp .jira.config.example.yaml .jira.config.yaml
# Edit with your JIRA URL, username, and API token

# 2. Fetch tasks by ticket IDs
report-gen fetch-tickets PROJ-123 PROJ-124 PROJ-125 -o tasks.yaml

# 3. Generate report with JIRA data
report-gen generate tasks.yaml -t feature_dev -o report.docx
```

**That's it!** All task data (title, status, assignee, dates, etc.) is automatically fetched from JIRA.

### Sync Existing Tasks

You can also sync existing data files with JIRA to update task information:

```bash
# Update tasks that have jira_id field
report-gen sync-jira feature_data.yaml
```

**What gets fetched:**
- Task title, description
- Status, priority, and assignee
- Due dates and target dates
- JIRA ticket IDs and labels

See the [JIRA Integration Guide](docs/jira-integration.md) for detailed setup and usage.

## Python API

Use programmatically in your Python code:

```python
from datetime import date
from report_template import FeatureDevReport, ReportGenerator, ReportType
from report_template.models import TeamMember, Task, Status, Priority

# Create report data
report = FeatureDevReport(
    title="OAuth2 Authentication Feature",
    project_name="MyApp",
    author="John Doe",
    feature_name="OAuth2 Auth System",
    summary="Implementing OAuth2 authentication with multiple providers",
    team_members=[
        TeamMember(name="John Doe", role="Lead Developer", email="john@example.com")
    ],
    tasks=[
        Task(title="Design auth flow", status=Status.COMPLETED, priority=Priority.HIGH)
    ]
)

# Generate report
generator = ReportGenerator()
generator.generate_to_file(
    report,
    ReportType.FEATURE_DEV,
    "output/my_report.md"
)
```

## Customization

### Custom Templates

Create your own templates:

```bash
# Copy built-in templates
mkdir my_templates
cp -r src/report_template/templates/* my_templates/

# Edit templates as needed
# my_templates/feature_dev.md.j2

# Use custom templates
report-gen generate data.yaml -t feature_dev -o report.md \
  --template-dir my_templates
```

### Custom Fields

Add project-specific data:

```yaml
# my_feature.yaml
title: "My Report"
project_name: "My Project"
# ... standard fields ...

custom_fields:
  jira_epic: "PROJ-123"
  estimated_cost: "$50,000"
  compliance: "GDPR Compliant"
  tech_stack: "Python, FastAPI, PostgreSQL"
```

Access in templates:

```jinja2
**JIRA Epic:** {{ custom_fields.jira_epic }}
**Estimated Cost:** {{ custom_fields.estimated_cost }}
```

## CLI Reference

### Generate Report

```bash
report-gen generate <data-file> -t <type> -o <output> [options]

Options:
  -t, --type       Report type (feature_dev, program_mgmt, engineering_init)
  -o, --output     Output file path
  -f, --format     Output format (markdown, html, pdf, docx) [auto-detected]
  --template-dir   Custom templates directory
  --template       Custom template name (not applicable for DOCX)
```

### Initialize Sample Data

```bash
report-gen init -t <type> -o <output> [options]

Options:
  -t, --type    Report type
  -o, --output  Output file path
  -f, --format  Data format (yaml, json) [default: yaml]
```

### Fetch Tasks from JIRA by Ticket IDs

```bash
report-gen fetch-tickets <JIRA-ID> [<JIRA-ID> ...] -o <output>

Examples:
  report-gen fetch-tickets PROJ-123 PROJ-124 -o tasks.yaml
  report-gen fetch-tickets AUTH-101 AUTH-102 AUTH-103 -o feature.yaml
```

### Sync Existing Data with JIRA

```bash
report-gen sync-jira <data-file>

Example:
  report-gen sync-jira my_feature.yaml
```

### List Templates

```bash
report-gen list-templates [--template-dir DIR]
```

## Examples

Check out the `examples/` directory:

- `feature_dev_example.py` - Complete feature development report example
- `sample_data/` - Sample YAML data files for each report type

Run an example:

```bash
cd examples
python feature_dev_example.py
```

## Documentation

- [Usage Guide](docs/usage.md) - Detailed usage instructions
- [JIRA Integration Guide](docs/jira-integration.md) - Sync tasks with JIRA server
- [Customization Guide](docs/customization.md) - Template customization and extensions
- [API Documentation](docs/api.md) - Python API reference (coming soon)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/report-template.git
cd report-template

# Install with development dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=report_template --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Project Structure

```
report-template/
├── src/
│   └── report_template/
│       ├── __init__.py
│       ├── models.py              # Pydantic data models
│       ├── generator.py           # Core report generator
│       ├── cli.py                 # Command-line interface
│       ├── formatters/            # Output formatters
│       │   ├── markdown.py
│       │   ├── html.py
│       │   ├── pdf.py
│       │   └── docx.py
│       └── templates/             # Jinja2 templates
│           ├── feature_dev.md.j2
│           ├── feature_dev.html.j2
│           ├── program_mgmt.md.j2
│           └── engineering_init.md.j2
├── tests/                         # Unit tests
├── examples/                      # Usage examples
├── docs/                          # Documentation
├── pyproject.toml                 # Project configuration
└── README.md
```

## Requirements

- Python 3.8+
- jinja2 >= 3.1.0
- pyyaml >= 6.0
- pydantic >= 2.0.0
- click >= 8.1.0
- markdown >= 3.4.0
- python-docx >= 1.0.0
- weasyprint >= 59.0 (optional, for PDF generation)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Use Cases

- **Development Teams**: Track feature development progress
- **Engineering Managers**: Generate status reports for stakeholders
- **Program Managers**: Create comprehensive program updates
- **DevOps Teams**: Document infrastructure initiatives
- **Technical Writers**: Maintain consistent documentation
- **QA Teams**: Document testing strategies and results

## Why Use report-template?

- **Consistency**: Standardized format across all reports
- **Time-Saving**: Generate professional reports in minutes
- **Version Control**: Keep reports in git with your code
- **Automation**: Integrate into CI/CD pipelines
- **Flexibility**: Customize to match your needs
- **Professional**: Beautiful, ready-to-present output

## Support

- [Issues](https://github.com/yourusername/report-template/issues) - Report bugs or request features
- [Discussions](https://github.com/yourusername/report-template/discussions) - Ask questions

## Roadmap

- [ ] Web UI for report generation
- [ ] Additional report types (retrospectives, incident reports)
- [ ] Integration with project management tools (Jira, GitHub)
- [ ] Report templates marketplace
- [ ] Multi-language support
- [ ] Real-time collaboration features

---

Made with ❤️ for better project documentation
