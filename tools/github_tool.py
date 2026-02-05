import requests
from .base import BaseTool

class GitHubTool(BaseTool):
    def execute(self, repo_name):
        """Fetches repo details from GitHub."""
        url = f"https://api.github.com/repos/{repo_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data.get("name"),
                "stars": data.get("stargazers_count"),
                "description": data.get("description"),
                "url": data.get("html_url")
            }
        return {"error": f"Repo '{repo_name}' not found or API error."}

    def get_definition(self):
        return {
            "name": "github_tool",
            "description": "Get details about a GitHub repository (stars, description).",
            "parameters": {"repo_name": "string (format: owner/repo)"}
        }