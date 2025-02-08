from __future__ import annotations

import requests  # type: ignore
from bs4 import BeautifulSoup


def search_web(query: str) -> str | None:
    """Search the web and return a brief summary."""
    url = f'https://www.google.com/search?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        snippet_tag = soup.find('span', class_='BNeawe')

        return snippet_tag.get_text(strip=True) if snippet_tag else None

    except requests.RequestException as e:
        return f'Failed to search the web: {e}"'  # This will always return str
