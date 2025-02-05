import requests
from bs4 import BeautifulSoup


def search_web(query: str) -> str:
    """Search the web and return a brief summary."""
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        snippet = soup.find("span", class_="BNeawe").text

        print(snippet)
        return snippet

    except Exception as e:
        return f"Failed to search the web: {e}"


search_web("python typing Optional?")
