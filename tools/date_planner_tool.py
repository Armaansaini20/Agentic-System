import requests
import os
from .base import BaseTool

class DatePlannerTool(BaseTool):
    def execute(self, location, category):
        api_key = os.getenv("TOMTOM_API_KEY")
        if not api_key:
            return {"error": "Missing TomTom API Key in .env"}

        # Use the Fuzzy Search endpoint
        query = f"{category} in {location}"
        url = f"https://api.tomtom.com/search/2/search/{query}.json"
        
        params = {
            "key": api_key,
            "limit": 3,
            "countrySet": "IN"
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200 and data.get('results'):
                top_spots = []
                for place in data['results']:
                    poi = place.get("poi", {})
                    addr = place.get("address", {})
                    
                    # FIX: Safely handle the distance field
                    raw_dist = place.get('dist')
                    dist_str = f"{raw_dist/1000:.1f}km" if raw_dist is not None else "Location found"
                    
                    top_spots.append({
                        "name": poi.get("name", "Unknown Venue"),
                        "category": poi.get("categories", ["Venue"])[0],
                        "address": addr.get("freeformAddress", "Address not available"),
                        "distance": dist_str
                    })
                return {"date_venues": top_spots}
            else:
                return {"error": "No venues found. Try a different category or be more specific with the city."}
        except Exception as e:
            return {"error": f"TomTom API failed: {str(e)}"}

    def get_definition(self):
        return {
            "name": "date_planner_tool",
            "description": "Finds real-world venues for dates in India (cafes, restaurants, etc.).",
            "parameters": {
                "location": "string (e.g., 'Indiranagar, Bangalore')",
                "category": "string (e.g., 'Coffee' or 'Pizza')"
            }
        }