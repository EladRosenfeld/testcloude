"""
Wikipedia API interaction module.

This module handles all communication with the Wikipedia API,
including fetching user contributions and handling pagination.
"""

import time
from typing import Generator
import requests
from tqdm import tqdm

import config


class WikipediaAPIError(Exception):
    """Custom exception for Wikipedia API errors."""
    pass


class WikipediaAPI:
    """
    Client for interacting with the Wikipedia API.

    Handles fetching user contributions with automatic pagination,
    rate limiting, and error handling.
    """

    def __init__(self, language: str = "en"):
        """
        Initialize the Wikipedia API client.

        Args:
            language: Wikipedia language code (default: "en" for English)
        """
        self.base_url = f"https://{language}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": config.USER_AGENT})

    def _make_request(self, params: dict) -> dict:
        """
        Make a request to the Wikipedia API with retry logic.

        Args:
            params: Query parameters for the API request

        Returns:
            JSON response from the API

        Raises:
            WikipediaAPIError: If the request fails after all retries
        """
        full_params = {**config.DEFAULT_PARAMS, **params}

        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.session.get(
                    self.base_url,
                    params=full_params,
                    timeout=config.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    raise WikipediaAPIError(
                        f"API error: {data['error'].get('info', 'Unknown error')}"
                    )

                return data

            except requests.RequestException as e:
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise WikipediaAPIError(f"Request failed: {e}")

        raise WikipediaAPIError("Max retries exceeded")

    def check_user_exists(self, username: str) -> bool:
        """
        Check if a Wikipedia user exists.

        Args:
            username: Wikipedia username to check

        Returns:
            True if user exists, False otherwise
        """
        params = {
            "list": "users",
            "ususers": username,
            "usprop": "editcount"
        }

        data = self._make_request(params)
        users = data.get("query", {}).get("users", [])

        if not users:
            return False

        return "missing" not in users[0]

    def get_user_info(self, username: str) -> dict:
        """
        Get basic information about a Wikipedia user.

        Args:
            username: Wikipedia username

        Returns:
            Dictionary with user information
        """
        params = {
            "list": "users",
            "ususers": username,
            "usprop": "editcount|registration|groups"
        }

        data = self._make_request(params)
        users = data.get("query", {}).get("users", [])

        if not users or "missing" in users[0]:
            raise WikipediaAPIError(f"User '{username}' not found")

        return users[0]

    def fetch_contributions(
        self,
        username: str,
        show_progress: bool = True
    ) -> list[dict]:
        """
        Fetch all contributions for a Wikipedia user.

        Uses pagination to retrieve all contributions, with optional
        progress bar display.

        Args:
            username: Wikipedia username
            show_progress: Whether to display a progress bar

        Returns:
            List of contribution dictionaries
        """
        contributions = []
        continue_token = None

        # First, get user info to estimate total edits
        user_info = self.get_user_info(username)
        total_edits = user_info.get("editcount", 0)

        if total_edits == 0:
            return []

        # Set up progress bar
        pbar = None
        if show_progress:
            pbar = tqdm(
                total=total_edits,
                desc=f"Fetching contributions for {username}",
                unit="edits"
            )

        try:
            while True:
                params = {
                    **config.USER_CONTRIBUTIONS_PARAMS,
                    "ucuser": username,
                }

                if continue_token:
                    params["uccontinue"] = continue_token

                data = self._make_request(params)

                batch = data.get("query", {}).get("usercontribs", [])
                contributions.extend(batch)

                if pbar:
                    pbar.update(len(batch))

                # Check for continuation
                if "continue" in data:
                    continue_token = data["continue"].get("uccontinue")
                    time.sleep(config.REQUEST_DELAY)
                else:
                    break

        finally:
            if pbar:
                pbar.close()

        return contributions

    def fetch_contributions_generator(
        self,
        username: str
    ) -> Generator[dict, None, None]:
        """
        Generator that yields contributions one at a time.

        Useful for processing large contribution lists without
        loading everything into memory.

        Args:
            username: Wikipedia username

        Yields:
            Individual contribution dictionaries
        """
        continue_token = None

        while True:
            params = {
                **config.USER_CONTRIBUTIONS_PARAMS,
                "ucuser": username,
            }

            if continue_token:
                params["uccontinue"] = continue_token

            data = self._make_request(params)

            for contrib in data.get("query", {}).get("usercontribs", []):
                yield contrib

            if "continue" in data:
                continue_token = data["continue"].get("uccontinue")
                time.sleep(config.REQUEST_DELAY)
            else:
                break

    def get_page_categories(self, titles: list[str]) -> dict[str, list[str]]:
        """
        Get categories for a list of Wikipedia pages.

        Args:
            titles: List of page titles

        Returns:
            Dictionary mapping page titles to their categories
        """
        # Wikipedia API limits titles per request
        batch_size = 50
        all_categories = {}

        for i in range(0, len(titles), batch_size):
            batch_titles = titles[i:i + batch_size]

            params = {
                "prop": "categories",
                "titles": "|".join(batch_titles),
                "cllimit": "max",
                "clshow": "!hidden"  # Exclude hidden categories
            }

            data = self._make_request(params)
            pages = data.get("query", {}).get("pages", [])

            for page in pages:
                title = page.get("title", "")
                categories = [
                    cat.get("title", "").replace("Category:", "")
                    for cat in page.get("categories", [])
                ]
                all_categories[title] = categories

            if i + batch_size < len(titles):
                time.sleep(config.REQUEST_DELAY)

        return all_categories


def fetch_user_contributions(username: str, show_progress: bool = True) -> list[dict]:
    """
    Convenience function to fetch all contributions for a user.

    Args:
        username: Wikipedia username
        show_progress: Whether to show progress bar

    Returns:
        List of contribution dictionaries
    """
    api = WikipediaAPI()
    return api.fetch_contributions(username, show_progress)
