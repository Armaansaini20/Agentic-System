from .base import BaseTool

class CompatibilityTool(BaseTool):
    def execute(self, user_interests, match_interests):
        """
        Simulates TrulyMadly's compatibility scoring logic.
        """
        # Common interests calculation
        user_set = set(user_interests.lower().split(", "))
        match_set = set(match_interests.lower().split(", "))
        common = list(user_set.intersection(match_set))
        
        # Calculate a mock score based on overlap
        score = 60 + (len(common) * 8)
        if score > 95: score = 98

        return {
            "compatibility_score": f"{score}%",
            "common_interests": common,
            "match_vibe": "High Energy" if "fitness" in match_interests or "travel" in match_interests else "Relaxed",
            "date_recommendation": "Based on your shared love for " + (common[0] if common else "exploration")
        }

    def get_definition(self):
        return {
            "name": "compatibility_tool",
            "description": "Analyzes interests between two users to calculate a TrulyMadly compatibility score and date ideas.",
            "parameters": {
                "user_interests": "string (comma separated list)",
                "match_interests": "string (comma separated list)"
            }
        }