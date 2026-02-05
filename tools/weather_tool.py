import requests
import os
from .base import BaseTool

class WeatherTool(BaseTool):
    def execute(self, city):
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return {"error": "Missing Weather API Key in .env file"}
        
        # Standard Current Weather endpoint
        url = "https://api.openweathermap.org/data/2.5/weather"
        
        # FIX: 'metric' must be in quotes as it is a string value for the API
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    "city": data.get("name"),
                    "temperature": data["main"].get("temp"),
                    "condition": data["weather"][0].get("description"),
                    "humidity": data["main"].get("humidity")
                }
            else:
                return {"error": f"API Error {response.status_code}: {data.get('message', 'Unknown error')}"}
        except Exception as e:
            return {"error": f"Connection error: {str(e)}"}

    def get_definition(self):
        return {
            "name": "weather_tool",
            "description": "Get current weather for a city including temperature and conditions.",
            "parameters": {"city": "string"}
        }