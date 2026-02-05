import concurrent.futures
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool

class ExecutorAgent:
    def __init__(self):
        # Initializing tools
        self.tools = {
            "github_tool": GitHubTool(),
            "weather_tool": WeatherTool()
        }

    def _execute_single_step(self, step):
        """Helper method to execute a single tool step safely."""
        tool_name = step.get("tool")
        args = step.get("args", {})
        
        if tool_name not in self.tools:
            return tool_name, {"error": f"Tool {tool_name} not found."}
        
        print(f"🔧 Parallel Executing: {tool_name}...")
        try:
            output = self.tools[tool_name].execute(**args)
            return tool_name, output
        except Exception as e:
            return tool_name, {"error": str(e)}

    def execute_plan(self, plan):
        results = {}
        steps = plan.get("steps", [])
        
        if not steps:
            return results

        # Using ThreadPoolExecutor to run tools in parallel
        # max_workers can be adjusted based on your API rate limits
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(steps)) as executor:
            # Map each step to a future (a promise of a result)
            future_to_step = {executor.submit(self._execute_single_step, step): step for step in steps}
            
            for future in concurrent.futures.as_completed(future_to_step):
                tool_name, output = future.result()
                results[tool_name] = output
        
        return results