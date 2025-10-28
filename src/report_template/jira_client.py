"""
JIRA integration module for fetching task data from JIRA server.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import requests

from report_template.models import Priority, Status


class JiraClient:
    """Client for interacting with JIRA API using Personal Access Token (PAT)."""

    def __init__(self, url: str, api_token: str):
        """
        Initialize JIRA client with Personal Access Token.

        Args:
            url: JIRA server URL (e.g., 'https://jiradc.ext.net.nokia.com')
            api_token: JIRA Personal Access Token (PAT)

        Note:
            This client uses Bearer token authentication with PAT.
            Basic authentication is not supported.
        """
        self.url = url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Fetch a JIRA issue by key.

        Args:
            issue_key: JIRA issue key (e.g., 'PROJ-123')

        Returns:
            Dictionary with issue data

        Raises:
            Exception: If issue not found or API error
        """
        api_url = f"{self.url}/rest/api/2/issue/{issue_key}?fields=*all"

        try:
            response = requests.get(api_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception(
                    f"Access denied to JIRA issue {issue_key}. "
                    "Check your Personal Access Token (PAT) permissions."
                ) from e
            elif e.response.status_code == 404:
                raise Exception(f"JIRA issue {issue_key} not found.") from e
            else:
                raise Exception(f"Failed to fetch JIRA issue {issue_key}: {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to JIRA: {str(e)}") from e

    def issue_to_task_data(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert JIRA issue to Task data format.

        Args:
            issue: JIRA issue dictionary

        Returns:
            Dictionary with task data compatible with Task model
        """
        fields = issue.get('fields', {})

        # Extract basic info
        task_data = {
            'title': fields.get('summary', 'Untitled'),
            'jira_id': issue.get('key', ''),
            'description': self._extract_description(fields.get('description')),
        }

        # Map status
        status = fields.get('status', {}).get('name', '')
        task_data['status'] = self._map_status(status)

        # Map priority
        priority = fields.get('priority', {}).get('name', '')
        task_data['priority'] = self._map_priority(priority)

        # Extract assignee
        assignee = fields.get('assignee')
        if assignee:
            task_data['assignee'] = assignee.get('displayName', assignee.get('name', ''))

        # Extract dates
        due_date = fields.get('duedate')
        if due_date:
            task_data['due_date'] = due_date

        # Try to get custom date fields (common field names)
        # You may need to adjust these based on your JIRA setup
        if 'customfield_10015' in fields:  # Common Sprint field
            task_data['target_start_date'] = self._extract_date(fields.get('customfield_10015'))

        if 'customfield_10016' in fields:  # Common target end date field
            task_data['target_end_date'] = self._extract_date(fields.get('customfield_10016'))

        # If start/end dates not found, try to use created and due dates
        if 'target_start_date' not in task_data:
            created = fields.get('created')
            if created:
                task_data['target_start_date'] = created.split('T')[0]

        if 'target_end_date' not in task_data and due_date:
            task_data['target_end_date'] = due_date

        # Extract tags/labels
        labels = fields.get('labels', [])
        if labels:
            task_data['tags'] = labels

        return task_data

    def _extract_description(self, description: Any) -> Optional[str]:
        """Extract description text from JIRA format."""
        if description is None:
            return None

        if isinstance(description, str):
            return description

        # Handle Atlassian Document Format (ADF)
        if isinstance(description, dict):
            # Simple text extraction from ADF
            content = description.get('content', [])
            text_parts = []
            for node in content:
                if node.get('type') == 'paragraph':
                    for child in node.get('content', []):
                        if child.get('type') == 'text':
                            text_parts.append(child.get('text', ''))
            return ' '.join(text_parts) if text_parts else None

        return str(description)

    def _extract_date(self, value: Any) -> Optional[str]:
        """Extract date from various JIRA date formats."""
        if value is None:
            return None

        if isinstance(value, str):
            # Try to parse ISO date
            try:
                if 'T' in value:
                    return value.split('T')[0]
                return value
            except:
                return None

        return None

    def _map_status(self, jira_status: str) -> str:
        """
        Map JIRA status to Task Status enum.

        Args:
            jira_status: JIRA status name

        Returns:
            Status enum value as string
        """
        status_lower = jira_status.lower()

        if status_lower in ['done', 'closed', 'resolved', 'completed']:
            return Status.COMPLETED.value
        elif status_lower in ['in progress', 'in development', 'in review']:
            return Status.IN_PROGRESS.value
        elif status_lower in ['blocked', 'impediment']:
            return Status.BLOCKED.value
        elif status_lower in ['on hold', 'paused']:
            return Status.ON_HOLD.value
        else:
            return Status.NOT_STARTED.value

    def _map_priority(self, jira_priority: str) -> str:
        """
        Map JIRA priority to Task Priority enum.

        Args:
            jira_priority: JIRA priority name

        Returns:
            Priority enum value as string
        """
        priority_lower = jira_priority.lower()

        if priority_lower in ['highest', 'critical', 'blocker']:
            return Priority.CRITICAL.value
        elif priority_lower in ['high']:
            return Priority.HIGH.value
        elif priority_lower in ['medium', 'normal']:
            return Priority.MEDIUM.value
        else:
            return Priority.LOW.value

    def sync_tasks(self, task_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sync task data with JIRA for tasks that have jira_id.

        Args:
            task_list: List of task dictionaries

        Returns:
            Updated list of task dictionaries with JIRA data
        """
        updated_tasks = []

        for task in task_list:
            jira_id = task.get('jira_id')

            if jira_id:
                try:
                    # Fetch from JIRA
                    issue = self.get_issue(jira_id)
                    jira_data = self.issue_to_task_data(issue)

                    # Merge JIRA data with existing task data
                    # Keep local data if JIRA field is empty
                    for key, value in jira_data.items():
                        if value is not None and value != '':
                            task[key] = value

                    print(f"✓ Synced {jira_id}: {task.get('title')}")

                except Exception as e:
                    print(f"✗ Failed to sync {jira_id}: {str(e)}")

            updated_tasks.append(task)

        return updated_tasks


def create_jira_client(config: Dict[str, str]) -> JiraClient:
    """
    Create JIRA client from configuration dictionary.

    Args:
        config: Dictionary with 'url' and 'api_token' keys
                'api_token' should be a Personal Access Token (PAT)

    Returns:
        JiraClient instance

    Raises:
        ValueError: If required config keys are missing
    """
    required_keys = ['url', 'api_token']
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        raise ValueError(f"Missing required JIRA config keys: {', '.join(missing_keys)}")

    return JiraClient(
        url=config['url'],
        api_token=config['api_token']
    )
