from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool

class ExecutorAgent:
    def __init__(self):
        self.tools = {
            "github_tool": GitHubTool(),
            "weather_tool": WeatherTool()
        }

    def execute_plan(self, plan):
        results = {}
        for step in plan.get("steps", []):
            tool_name = step.get("tool")
            args = step.get("args", {})
            
            if tool_name in self.tools:
                print(f"🔧 Executing {tool_name} with {args}...")
                try:
                    output = self.tools[tool_name].execute(**args)
                    results[tool_name] = output
                except Exception as e:
                    results[tool_name] = {"error": str(e)}
            else:
                print(f"⚠️ Tool {tool_name} not found.")
        
        return results