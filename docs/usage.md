# Usage Guide

This guide covers how to use the report-template package to generate professional project reports.

## Installation

```bash
# Install from source
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Using the CLI

The easiest way to generate reports is using the command-line interface:

```bash
# Step 1: Create a sample data file
report-gen init -t feature_dev -o my_feature.yaml

# Step 2: Edit the YAML file with your data
# (Use your favorite text editor)

# Step 3: Generate a report
report-gen generate my_feature.yaml -t feature_dev -o report.md
```

### Using Python

You can also generate reports programmatically:

```python
from datetime import date
from report_template import FeatureDevReport, ReportGenerator, ReportType
from report_template.models import TeamMember, Task, Status, Priority

# Create report data
report = FeatureDevReport(
    title="My Feature Report",
    project_name="My Project",
    author="Your Name",
    feature_name="New Feature",
    summary="Brief description of the feature",
    team_members=[
        TeamMember(name="John Doe", role="Developer", email="john@example.com")
    ],
    tasks=[
        Task(
            title="Implement feature X",
            status=Status.IN_PROGRESS,
            priority=Priority.HIGH
        )
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

## Report Types

### Feature Development Reports

Use for documenting feature development efforts:

```bash
report-gen init -t feature_dev -o feature.yaml
report-gen generate feature.yaml -t feature_dev -o feature_report.md
```

Key sections:
- Team and objectives
- Technical approach and architecture
- Tasks and milestones
- Testing and deployment plans
- Risks and dependencies

### Program Management Reports

Use for program-level status reporting:

```bash
report-gen init -t program_mgmt -o program.yaml
report-gen generate program.yaml -t program_mgmt -o program_report.md
```

Key sections:
- Executive summary
- Stakeholders and team
- KPIs and milestones
- Achievements and challenges
- Budget and decisions needed

### Engineering Initiative Reports

Use for documenting engineering initiatives:

```bash
report-gen init -t engineering_init -o initiative.yaml
report-gen generate initiative.yaml -t engineering_init -o initiative_report.md
```

Key sections:
- Objectives and scope
- Technical details and architecture
- Implementation phases
- Success criteria
- Impact analysis and rollout strategy

## Output Formats

### Markdown

Default format, great for version control:

```bash
report-gen generate data.yaml -t feature_dev -o report.md
# Or explicitly:
report-gen generate data.yaml -t feature_dev -o report.md -f markdown
```

### HTML

Professional web format with styling:

```bash
report-gen generate data.yaml -t feature_dev -o report.html -f html
```

### PDF

Print-ready format (requires WeasyPrint):

```bash
# Install WeasyPrint first
pip install weasyprint

# Generate PDF
report-gen generate data.yaml -t feature_dev -o report.pdf -f pdf
```

### Word Document (DOCX)

Microsoft Word format, perfect for email distribution:

```bash
report-gen generate data.yaml -t feature_dev -o report.docx -f docx
# Or let it auto-detect from extension:
report-gen generate data.yaml -t feature_dev -o report.docx
```

**Benefits of DOCX format:**
- Easy to email to stakeholders
- Compatible with Microsoft Word, Google Docs, LibreOffice
- Can be further edited and customized
- Works well in corporate environments
- Professional formatting with tables and styles
- No additional dependencies required

**Note:** DOCX reports are generated programmatically and don't use Jinja2 templates. They automatically include all report sections with professional formatting.

## Data File Formats

### YAML (Recommended)

More human-readable and easier to edit:

```yaml
title: "My Report"
project_name: "My Project"
author: "Your Name"
summary: "Description here"
team_members:
  - name: "John Doe"
    role: "Developer"
```

### JSON

Machine-friendly format:

```json
{
  "title": "My Report",
  "project_name": "My Project",
  "author": "Your Name",
  "summary": "Description here",
  "team_members": [
    {"name": "John Doe", "role": "Developer"}
  ]
}
```

## Advanced Usage

### Custom Templates

Create your own templates directory:

```bash
mkdir my_templates
cp -r src/report_template/templates/* my_templates/
# Edit templates as needed

# Use custom templates
report-gen generate data.yaml -t feature_dev -o report.md \
  --template-dir my_templates
```

### Custom Template for Generation

Use a specific template file:

```bash
report-gen generate data.yaml -t feature_dev -o report.md \
  --template my_custom_template.md.j2
```

### List Available Templates

See what templates are available:

```bash
report-gen list-templates

# With custom directory
report-gen list-templates --template-dir my_templates
```

### Python API - Custom Filters

Add custom Jinja2 filters:

```python
from report_template import ReportGenerator

def custom_filter(value):
    return value.upper()

generator = ReportGenerator(
    custom_filters={'upper': custom_filter}
)
```

## Examples

See the `examples/` directory for complete examples:

- `feature_dev_example.py` - Full feature development report
- `sample_data/` - Example data files for each report type

Run examples:

```bash
cd examples
python feature_dev_example.py
```

## Tips

1. **Start with init**: Always use `report-gen init` to create a template file
2. **Version control**: Keep your YAML data files in git for history
3. **Automation**: Use in CI/CD pipelines to generate reports automatically
4. **Custom fields**: Use the `custom_fields` dictionary for additional data
5. **Templates**: Customize templates to match your organization's style

## Troubleshooting

### PDF Generation Issues

If PDF generation fails:

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3-pip python3-cffi python3-brotli \
  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0

# Install WeasyPrint
pip install weasyprint
```

### Template Not Found

Ensure the template exists:

```bash
report-gen list-templates
```

### Validation Errors

Check your data file matches the required schema. Use `report-gen init` to see required fields.

## Next Steps

- Read [customization.md](customization.md) for template customization
- Check out the [examples](../examples/) directory
- See the API documentation for advanced usage
