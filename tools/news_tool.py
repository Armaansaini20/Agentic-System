import requests
import os
from .base import BaseTool

class NewsTool(BaseTool):
    def execute(self, query):
        api_key = os.getenv("NEWS_API_KEY")
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                articles = data.get("articles", [])
                return [{"title": a["title"], "source": a["source"]["name"], "url": a["url"]} for a in articles]
            return {"error": data.get("message", "Failed to fetch news")}
        except Exception as e:
            return {"error": str(e)}

    def get_definition(self):
        return {
            "name": "news_tool",
            "description": "Search for the latest news articles on a specific topic.",
            "parameters": {"query": "string"}
        }