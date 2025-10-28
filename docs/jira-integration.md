# JIRA Integration Guide

Automatically fetch and sync task data from your JIRA server to keep reports up-to-date.

## Features

- **Automatic Status Sync**: Fetch current status, assignee, and priorities from JIRA
- **JQL Queries**: Fetch tasks using powerful JIRA Query Language
- **Batch Updates**: Sync multiple tasks at once
- **Custom Field Mapping**: Configure which JIRA fields map to task fields

## Setup

### 1. Install Dependencies

The JIRA integration uses the `atlassian-python-api` library:

```bash
pip install atlassian-python-api
# Or install all dependencies
pip install -e .
```

### 2. Create JIRA Configuration

Copy the example configuration file:

```bash
cp .jira.config.example.yaml .jira.config.yaml
```

Edit `.jira.config.yaml` with your JIRA details:

```yaml
jira:
  url: "https://your-domain.atlassian.net"
  username: "your-email@example.com"
  api_token: "your-api-token-here"
```

### 3. Generate JIRA API Token

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label (e.g., "report-template")
4. Copy the token to your `.jira.config.yaml`

**Security Note**: Never commit `.jira.config.yaml` to version control! It's already in `.gitignore`.

## Usage

### Sync Existing Tasks

Update tasks in your data file with latest data from JIRA:

```bash
# Sync tasks that have jira_id field
report-gen sync-jira feature_data.yaml

# Save to a new file
report-gen sync-jira feature_data.yaml -o feature_data_synced.yaml

# Use custom config file
report-gen sync-jira feature_data.yaml --config ~/my-jira-config.yaml
```

**What gets synced:**
- Task title (summary)
- Status
- Priority
- Assignee
- Due date
- Description
- Labels/tags
- Start and end dates (if configured)

### Fetch Tasks from JIRA

Create a new data file with tasks fetched directly from JIRA using JQL:

```bash
# Fetch tasks from current sprint
report-gen fetch-jira "project = MYPROJ AND sprint in openSprints()" -o tasks.yaml

# Fetch all high-priority bugs
report-gen fetch-jira "project = MYPROJ AND type = Bug AND priority = High" -o bugs.yaml

# Fetch in-progress tasks assigned to you
report-gen fetch-jira "project = MYPROJ AND assignee = currentUser() AND status = 'In Progress'" -o my_tasks.yaml

# Limit number of results
report-gen fetch-jira "project = MYPROJ" -o tasks.yaml --max-results 20
```

Then generate a report:

```bash
report-gen generate tasks.yaml -t feature_dev -o report.md
```

## Workflow Examples

### Weekly Sprint Reports

```bash
#!/bin/bash
# Generate weekly sprint report with live JIRA data

# Fetch current sprint tasks
report-gen fetch-jira "project = MYPROJ AND sprint in openSprints()" -o sprint_tasks.yaml

# Edit the YAML file to add additional context
# (team members, objectives, technical approach, etc.)
vim sprint_tasks.yaml

# Generate the report
report-gen generate sprint_tasks.yaml -t feature_dev -o sprint_report.md
report-gen generate sprint_tasks.yaml -t feature_dev -o sprint_report.docx
```

### Update Existing Report

```bash
#!/bin/bash
# Update an existing report with latest JIRA data

# Sync with JIRA
report-gen sync-jira feature_report_data.yaml

# Regenerate reports
report-gen generate feature_report_data.yaml -t feature_dev -o report.md
report-gen generate feature_report_data.yaml -t feature_dev -o report.docx
```

### Monthly Program Reports

```bash
#!/bin/bash
# Generate monthly program report from JIRA

# Fetch all completed tasks from last month
report-gen fetch-jira "project = MYPROJ AND status = Done AND resolved >= -30d" -o completed_tasks.yaml

# Add program-level context and generate report
# Edit completed_tasks.yaml to add:
# - program_name
# - stakeholders
# - key_achievements
# - etc.

report-gen generate completed_tasks.yaml -t program_mgmt -o monthly_report.pdf
```

## JQL Query Examples

### By Status

```bash
# All open tasks
report-gen fetch-jira "project = MYPROJ AND status != Done" -o open_tasks.yaml

# Blocked tasks
report-gen fetch-jira "project = MYPROJ AND status = Blocked" -o blocked.yaml
```

### By Sprint

```bash
# Current sprint
report-gen fetch-jira "project = MYPROJ AND sprint in openSprints()" -o current_sprint.yaml

# Specific sprint
report-gen fetch-jira "project = MYPROJ AND sprint = 'Sprint 10'" -o sprint10.yaml
```

### By Team/Person

```bash
# Your tasks
report-gen fetch-jira "assignee = currentUser() AND status != Done" -o my_tasks.yaml

# Team tasks
report-gen fetch-jira "project = MYPROJ AND assignee in (user1, user2, user3)" -o team_tasks.yaml
```

### By Date

```bash
# Created in last 7 days
report-gen fetch-jira "project = MYPROJ AND created >= -7d" -o recent_tasks.yaml

# Due this week
report-gen fetch-jira "project = MYPROJ AND due >= startOfWeek() AND due <= endOfWeek()" -o due_this_week.yaml
```

### Complex Queries

```bash
# High priority in-progress backend tasks
report-gen fetch-jira "project = MYPROJ AND priority in (High, Critical) AND status = 'In Progress' AND labels = backend" -o backend_high_priority.yaml
```

## Field Mapping

### Default Mappings

| JIRA Field | Task Field | Notes |
|------------|------------|-------|
| Summary | title | Issue title |
| Key | jira_id | Issue key (e.g., PROJ-123) |
| Status | status | Mapped to Status enum |
| Priority | priority | Mapped to Priority enum |
| Assignee | assignee | Display name |
| Due Date | due_date | ISO format |
| Description | description | Text extracted |
| Labels | tags | List of labels |

### Status Mapping

| JIRA Status | Task Status |
|-------------|-------------|
| Done, Closed, Resolved, Completed | Completed |
| In Progress, In Development, In Review | In Progress |
| Blocked, Impediment | Blocked |
| On Hold, Paused | On Hold |
| Others | Not Started |

### Priority Mapping

| JIRA Priority | Task Priority |
|---------------|---------------|
| Highest, Critical, Blocker | Critical |
| High | High |
| Medium, Normal | Medium |
| Low, Lowest, Trivial | Low |

### Custom Fields

JIRA custom fields can be configured in `.jira.config.yaml`:

```yaml
jira:
  url: "https://your-domain.atlassian.net"
  username: "your-email@example.com"
  api_token: "your-api-token-here"

# Optional: Custom field mappings
field_mappings:
  target_start_date: "customfield_10015"
  target_end_date: "customfield_10016"
```

To find your custom field IDs, inspect a JIRA issue via API:
```bash
curl -u email@example.com:api_token \
  https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123
```

## Troubleshooting

### Authentication Errors

**Problem**: `401 Unauthorized` or `403 Forbidden`

**Solutions**:
- Verify your API token is correct
- Ensure username/email matches your JIRA account
- Check if your JIRA URL is correct (should end with `.atlassian.net` for cloud)
- Regenerate API token if expired

### Connection Errors

**Problem**: Cannot connect to JIRA server

**Solutions**:
- Check your internet connection
- Verify JIRA URL is correct and accessible
- Check if you're behind a corporate proxy (may need proxy configuration)

### JQL Syntax Errors

**Problem**: `JQL query parse error`

**Solutions**:
- Test your JQL in JIRA's web interface first (Filters → Advanced)
- Ensure field names are correct and in quotes if they contain spaces
- Use proper JQL functions (e.g., `openSprints()`, `currentUser()`)

### No Tasks Found

**Problem**: Query returns no results

**Solutions**:
- Verify the project key is correct
- Check if you have permission to view the project
- Simplify the query to debug (start with just `project = MYPROJ`)
- Verify the sprint/version/component names are exact matches

### Custom Fields Not Syncing

**Problem**: Start/end dates not syncing from JIRA

**Solutions**:
- Custom fields vary by JIRA instance
- Find your custom field IDs using the JIRA API
- Configure field mappings in `.jira.config.yaml`
- The JIRA client provides sensible defaults but may need customization

## Python API

Use the JIRA client directly in Python:

```python
from report_template.jira_client import JiraClient

# Initialize client
client = JiraClient(
    url="https://your-domain.atlassian.net",
    username="your-email@example.com",
    api_token="your-api-token"
)

# Get a single issue
issue = client.get_issue("PROJ-123")
task_data = client.issue_to_task_data(issue)

# Fetch multiple issues with JQL
tasks = client.fetch_tasks_by_jql("project = MYPROJ AND sprint in openSprints()")

# Sync existing tasks
updated_tasks = client.sync_tasks(existing_tasks)
```

## Best Practices

1. **Keep Config Secure**: Never commit `.jira.config.yaml` to version control
2. **Use Specific JQL**: Narrow queries fetch faster and are more accurate
3. **Sync Before Reports**: Run `sync-jira` before generating reports for latest data
4. **Version Control Data**: Keep YAML data files in git for report history
5. **Automate with Scripts**: Create bash scripts for regular report generation
6. **Test Queries**: Test JQL queries in JIRA web UI before using in CLI

## Security

- API tokens should be treated like passwords
- Use separate API tokens for different purposes (easier to revoke)
- Consider using environment variables for sensitive data:
  ```bash
  export JIRA_API_TOKEN="your-token"
  # Then reference in scripts
  ```
- Rotate API tokens periodically
- Revoke tokens when no longer needed

## Resources

- [JIRA Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [JQL Documentation](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-searching-in-jira-cloud/)
- [API Token Management](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- [atlassian-python-api Documentation](https://atlassian-python-api.readthedocs.io/)
