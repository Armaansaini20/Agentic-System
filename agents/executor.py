import concurrent.futures
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
# Import your other tools as well
from tools.news_tool import NewsTool
from tools.currency_tool import CurrencyTool
from tools.compatibility_tool import CompatibilityTool
from tools.date_planner_tool import DatePlannerTool

class ExecutorAgent:
    def __init__(self):
        # Initializing tools
        self.tools = {
            "github_tool": GitHubTool(),
            "weather_tool": WeatherTool(),
            "news_tool": NewsTool(),
            "currency_tool": CurrencyTool(),
            "compatibility_tool": CompatibilityTool(),
            "date_planner_tool": DatePlannerTool()
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

    def execute_plan(self, plan_input):
        """
        Executes the plan. 
        Handles both a raw dictionary plan or a (plan, metadata) tuple.
        """
        results = {}
        
        # --- FIX START: Handle Tuple vs Dictionary ---
        if isinstance(plan_input, tuple):
            plan = plan_input[0]  # Extract the dictionary from the (plan, metadata) tuple
        else:
            plan = plan_input
        # --- FIX END ---

        steps = plan.get("steps", []) if isinstance(plan, dict) else []
        
        if not steps:
            print("⚠️ No steps found in plan.")
            return results

        # Using ThreadPoolExecutor to run tools in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(steps)) as executor:
            future_to_step = {executor.submit(self._execute_single_step, step): step for step in steps}
            
            for future in concurrent.futures.as_completed(future_to_step):
                tool_name, output = future.result()
                results[tool_name] = output
        
        return results