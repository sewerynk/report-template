# Customization Guide

Learn how to customize templates, add new report types, and extend the report-template system.

## Template Customization

### Understanding Templates

Templates use Jinja2 syntax. Each template has access to all fields from the report data model.

### Creating Custom Templates

1. **Copy existing templates**:

```bash
mkdir my_templates
cp -r src/report_template/templates/* my_templates/
```

2. **Edit the template**:

```jinja2
# my_templates/feature_dev.md.j2

# {{ title }}

**Project:** {{ project_name }}
**Date:** {{ date|date }}

## Custom Section

This is my custom section with {{ custom_fields.my_field }}.

{% for task in tasks %}
- {{ task.title }} ({{ task.status.value }})
{% endfor %}
```

3. **Use your template**:

```bash
report-gen generate data.yaml -t feature_dev -o report.md \
  --template-dir my_templates
```

### Template Variables

All report data is available in templates:

#### Feature Development Reports

```jinja2
{{ title }}              - Report title
{{ project_name }}       - Project name
{{ author }}             - Author name
{{ date }}               - Report date
{{ feature_name }}       - Feature name
{{ repository }}         - Repository URL
{{ branch }}             - Git branch
{{ sprint }}             - Sprint name
{{ summary }}            - Executive summary
{{ technical_approach }} - Technical description
{{ architecture_notes }} - Architecture notes
{{ testing_strategy }}   - Testing strategy
{{ deployment_plan }}    - Deployment plan
{{ progress_notes }}     - Progress notes

{# Lists #}
{% for member in team_members %}
  {{ member.name }}
  {{ member.role }}
  {{ member.email }}
{% endfor %}

{% for task in tasks %}
  {{ task.title }}
  {{ task.assignee }}
  {{ task.status.value }}
  {{ task.priority.value }}
  {{ task.due_date }}
{% endfor %}

{% for milestone in milestones %}
  {{ milestone.name }}
  {{ milestone.target_date }}
  {{ milestone.status.value }}
  {{ milestone.completion_percentage }}
{% endfor %}

{% for risk in risks %}
  {{ risk.description }}
  {{ risk.impact.value }}
  {{ risk.likelihood.value }}
  {{ risk.mitigation }}
  {{ risk.owner }}
{% endfor %}
```

### Jinja2 Filters

Available filters:

```jinja2
{{ date|date }}              - Format date as YYYY-MM-DD
{{ percentage|percentage }}  - Add % symbol
{{ value|upper }}            - Uppercase
{{ value|lower }}            - Lowercase
{{ value|title }}            - Title case
```

### Custom Filters

Add your own filters:

```python
from report_template import ReportGenerator

def format_currency(value):
    return f"${value:,.2f}"

def highlight_critical(value):
    if value == "Critical":
        return f"🔴 {value}"
    return value

generator = ReportGenerator(
    custom_filters={
        'currency': format_currency,
        'highlight': highlight_critical,
    }
)
```

Use in templates:

```jinja2
Budget: {{ budget_value|currency }}
Priority: {{ task.priority.value|highlight }}
```

## Styling

### Markdown Styling

For Markdown, add formatting:

```jinja2
# {{ title }}

> {{ summary }}

**Status**: {{ status.value }}

| Column 1 | Column 2 |
|----------|----------|
{% for item in items %}
| {{ item.name }} | {{ item.value }} |
{% endfor %}
```

### HTML Styling

Customize CSS in HTML templates:

```html
<style>
    .custom-section {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 5px;
    }

    .priority-critical {
        color: red;
        font-weight: bold;
    }
</style>

<div class="custom-section">
    <h2>{{ section_title }}</h2>
    <p>{{ section_content }}</p>
</div>
```

### PDF Styling

PDF generation uses HTML templates, so style with CSS:

```html
<style>
    @page {
        size: A4;
        margin: 2cm;
    }

    h1 {
        color: #2c3e50;
        page-break-before: always;
    }

    .no-break {
        page-break-inside: avoid;
    }
</style>
```

## Adding Custom Fields

### In Data Files

Add any custom fields to your data:

```yaml
title: "My Report"
project_name: "My Project"
# ... other fields ...

custom_fields:
  compliance_status: "GDPR Compliant"
  estimated_cost: "$50,000"
  tech_stack: "Python, FastAPI, PostgreSQL"
  jira_epic: "PROJ-123"
```

### In Templates

Access custom fields:

```jinja2
## Additional Information

**Compliance:** {{ custom_fields.compliance_status }}
**Estimated Cost:** {{ custom_fields.estimated_cost }}
**Tech Stack:** {{ custom_fields.tech_stack }}
**JIRA Epic:** [{{ custom_fields.jira_epic }}](https://jira.example.com/browse/{{ custom_fields.jira_epic }})
```

## Creating New Report Types

### Step 1: Define Data Model

Create a new model in `src/report_template/models.py`:

```python
class CustomReport(ReportData):
    """Model for custom reports."""

    report_specific_field: str
    custom_metrics: Dict[str, Any] = Field(default_factory=dict)
    custom_list: List[str] = Field(default_factory=list)
```

### Step 2: Create Template

Create `custom_report.md.j2`:

```jinja2
# {{ title }}

**{{ report_specific_field }}**

## Metrics

{% for metric, value in custom_metrics.items() %}
- {{ metric }}: {{ value }}
{% endfor %}

## Items

{% for item in custom_list %}
- {{ item }}
{% endfor %}
```

### Step 3: Update Enum

Add to `ReportType` enum:

```python
class ReportType(str, Enum):
    FEATURE_DEV = "feature_dev"
    PROGRAM_MGMT = "program_mgmt"
    ENGINEERING_INIT = "engineering_init"
    CUSTOM = "custom_report"  # Add this
```

### Step 4: Update CLI

Add to `cli.py` model map:

```python
model_map = {
    ReportType.FEATURE_DEV: FeatureDevReport,
    ReportType.PROGRAM_MGMT: ProgramMgmtReport,
    ReportType.ENGINEERING_INIT: EngineeringInitReport,
    ReportType.CUSTOM: CustomReport,  # Add this
}
```

## Template Inheritance

Create base templates:

```jinja2
{# base.md.j2 #}
# {{ title }}

**Project:** {{ project_name }}
**Author:** {{ author }}
**Date:** {{ date|date }}

---

{% block content %}
{# Child templates override this #}
{% endblock %}

---

*Generated on {{ date|date }}*
```

Extend in child templates:

```jinja2
{# custom_report.md.j2 #}
{% extends "base.md.j2" %}

{% block content %}
## Custom Content

{{ custom_field }}
{% endblock %}
```

## Conditional Sections

Show/hide sections based on data:

```jinja2
{% if risks %}
## Risks

{% for risk in risks %}
### {{ risk.description }}
- **Impact:** {{ risk.impact.value }}
{% endfor %}
{% else %}
No risks identified.
{% endif %}

{% if team_members|length > 5 %}
## Large Team Notice
This project has a large team of {{ team_members|length }} members.
{% endif %}
```

## Macros for Reusability

Define reusable components:

```jinja2
{# macros.j2 #}
{% macro status_badge(status) %}
{% if status.value == "Completed" %}
✅ {{ status.value }}
{% elif status.value == "In Progress" %}
🔄 {{ status.value }}
{% else %}
⏸️ {{ status.value }}
{% endif %}
{% endmacro %}

{% macro task_table(tasks) %}
| Task | Status | Priority |
|------|--------|----------|
{% for task in tasks %}
| {{ task.title }} | {{ status_badge(task.status) }} | {{ task.priority.value }} |
{% endfor %}
{% endmacro %}
```

Use macros:

```jinja2
{% import 'macros.j2' as macros %}

## Tasks
{{ macros.task_table(tasks) }}
```

## Best Practices

1. **Keep templates DRY**: Use macros and template inheritance
2. **Provide defaults**: Use `or` for optional fields: `{{ field or 'N/A' }}`
3. **Format dates consistently**: Always use the `date` filter
4. **Handle empty lists**: Check `{% if list %}` before iterating
5. **Add comments**: Document complex template logic
6. **Test templates**: Generate reports with various data to ensure they work
7. **Version control**: Keep templates in git alongside code

## Examples

See complete customization examples:

- `examples/custom_template_example.py` - Custom template usage
- `examples/custom_filters_example.py` - Custom filter implementation
- `templates/` - Built-in template examples

## Troubleshooting

### Template Syntax Errors

Check Jinja2 syntax:
- Ensure all `{% %}` blocks are closed
- Match opening/closing tags (`{% if %}...{% endif %}`)
- Use correct filter syntax: `{{ value|filter }}`

### Missing Data

Provide defaults:

```jinja2
{{ field or 'Not specified' }}
{{ field|default('N/A') }}
```

### HTML Rendering Issues

- Escape HTML when needed: `{{ field|e }}`
- Use `|safe` for trusted HTML: `{{ html_content|safe }}`

## Next Steps

- Review [usage.md](usage.md) for basic usage
- Check [examples](../examples/) for working code
- Explore built-in templates for inspiration
