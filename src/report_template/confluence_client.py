"""
Confluence integration module for pushing reports to Confluence pages.
"""

from typing import Any, Dict, Optional
import requests


class ConfluenceClient:
    """Client for interacting with Confluence API using Personal Access Token (PAT)."""

    def __init__(self, url: str, api_token: str):
        """
        Initialize Confluence client with Personal Access Token.

        Args:
            url: Confluence server URL (e.g., 'https://confluence.example.com')
            api_token: Confluence Personal Access Token (PAT)

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

    def get_page_by_title(self, space_key: str, title: str) -> Optional[Dict[str, Any]]:
        """
        Get a Confluence page by title in a specific space.

        Args:
            space_key: Confluence space key (e.g., 'PROJ')
            title: Page title

        Returns:
            Page data if found, None otherwise

        Raises:
            Exception: If API error occurs
        """
        api_url = f"{self.url}/rest/api/content"
        params = {
            "spaceKey": space_key,
            "title": title,
            "expand": "version,body.storage"
        }

        try:
            response = requests.get(api_url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                return data["results"][0]
            return None

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get page '{title}': {str(e)}") from e

    def create_page(
        self,
        space_key: str,
        title: str,
        content: str,
        parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new Confluence page.

        Args:
            space_key: Confluence space key (e.g., 'PROJ')
            title: Page title
            content: Page content in Confluence storage format (HTML)
            parent_id: Optional parent page ID

        Returns:
            Created page data

        Raises:
            Exception: If page creation fails
        """
        api_url = f"{self.url}/rest/api/content"

        page_data = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }

        if parent_id:
            page_data["ancestors"] = [{"id": parent_id}]

        try:
            response = requests.post(
                api_url,
                headers=self.headers,
                json=page_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise Exception(
                    f"Failed to create page '{title}': Invalid data. "
                    "Check that space key and content are valid."
                ) from e
            elif e.response.status_code == 403:
                raise Exception(
                    f"Access denied. Check your Confluence PAT has write permissions to space '{space_key}'."
                ) from e
            else:
                raise Exception(f"Failed to create page '{title}': {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Confluence: {str(e)}") from e

    def update_page(
        self,
        page_id: str,
        title: str,
        content: str,
        version: int
    ) -> Dict[str, Any]:
        """
        Update an existing Confluence page.

        Args:
            page_id: Page ID
            title: Page title (can be updated)
            content: New page content in Confluence storage format (HTML)
            version: Current version number (will be incremented)

        Returns:
            Updated page data

        Raises:
            Exception: If page update fails
        """
        api_url = f"{self.url}/rest/api/content/{page_id}"

        page_data = {
            "version": {"number": version + 1},
            "title": title,
            "type": "page",
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }

        try:
            response = requests.put(
                api_url,
                headers=self.headers,
                json=page_data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                raise Exception(
                    f"Version conflict for page '{title}'. "
                    "The page may have been updated by someone else. Try again."
                ) from e
            else:
                raise Exception(f"Failed to update page '{title}': {str(e)}") from e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Confluence: {str(e)}") from e

    def create_or_update_page(
        self,
        space_key: str,
        title: str,
        content: str,
        parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new page or update if it already exists.

        Args:
            space_key: Confluence space key (e.g., 'PROJ')
            title: Page title
            content: Page content in Confluence storage format (HTML)
            parent_id: Optional parent page ID (used only when creating)

        Returns:
            Page data (created or updated)

        Raises:
            Exception: If operation fails
        """
        # Check if page exists
        existing_page = self.get_page_by_title(space_key, title)

        if existing_page:
            # Update existing page
            page_id = existing_page["id"]
            version = existing_page["version"]["number"]
            print(f"Updating existing page '{title}' (ID: {page_id}, Version: {version})")
            return self.update_page(page_id, title, content, version)
        else:
            # Create new page
            print(f"Creating new page '{title}' in space '{space_key}'")
            return self.create_page(space_key, title, content, parent_id)

    def get_page_url(self, page_data: Dict[str, Any]) -> str:
        """
        Get the web URL for a Confluence page.

        Args:
            page_data: Page data from create/update response

        Returns:
            Full URL to the page
        """
        page_id = page_data.get("id")
        # Construct URL - may need adjustment based on your Confluence setup
        return f"{self.url}/pages/viewpage.action?pageId={page_id}"


def create_confluence_client(config: Dict[str, str]) -> ConfluenceClient:
    """
    Create Confluence client from configuration dictionary.

    Args:
        config: Dictionary with 'url' and 'api_token' keys
                'api_token' should be a Personal Access Token (PAT)

    Returns:
        ConfluenceClient instance

    Raises:
        ValueError: If required config keys are missing
    """
    required_keys = ['url', 'api_token']
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        raise ValueError(f"Missing required Confluence config keys: {', '.join(missing_keys)}")

    return ConfluenceClient(
        url=config['url'],
        api_token=config['api_token']
    )
