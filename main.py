import json
import os
from termcolor import colored
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

# Import all tools
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool
from tools.currency_tool import CurrencyTool
from tools.compatibility_tool import CompatibilityTool
from tools.date_planner_tool import DatePlannerTool

def main():
    print(colored("🤖 AI Operations Assistant (Enhanced) Initialized", "cyan", attrs=['bold']))
    print(colored("Tools Loaded: GitHub, Weather, News, Currency\n", "white"))
    
    # 1. Inputs
    user_query = input(colored("📝 Enter your request: ", "yellow"))
    
    # 2. Planning
    planner = PlannerAgent()
    # Register all 4 tool definitions for the Planner to see
    tool_defs = [
        GitHubTool().get_definition(), 
        WeatherTool().get_definition(),
        NewsTool().get_definition(),
        CurrencyTool().get_definition(),
        CompatibilityTool().get_definition(),
        DatePlannerTool().get_definition()
    ]
    
    print(colored("\n🧠 Planner thinking...", "magenta"))
    plan = planner.create_plan(user_query, tool_defs)
    print(colored(f"📋 Plan created: {json.dumps(plan, indent=2)}", "blue"))

    # 3. Execution
    executor = ExecutorAgent()
    # Ensure Executor has all tool classes mapped
    executor.tools = {
        "github_tool": GitHubTool(),
        "weather_tool": WeatherTool(),
        "news_tool": NewsTool(),
        "currency_tool": CurrencyTool(),
        "compatibility_tool": CompatibilityTool(),
        "date_planner_tool": DatePlannerTool()
    }
    
    print(colored("\n⚙️ Executor running...", "magenta"))
    execution_results = executor.execute_plan(plan)
    print(colored(f"📦 Raw Results: {json.dumps(execution_results, indent=2)}", "green"))

    # 4. Verification
    verifier = VerifierAgent()
    print(colored("\n🔍 Verifier checking...", "magenta"))
    final_output = verifier.verify_and_respond(user_query, execution_results)
    
    # Final Output with Safety Check
    try:
        parsed_output = json.loads(final_output)
        answer = parsed_output.get('final_answer', "The assistant encountered an error processing the results.")
        print(colored("\n✅ FINAL ANSWER:", "cyan", attrs=['bold']))
        print(answer)
    except json.JSONDecodeError:
        print(colored("\n❌ Error: The agent returned invalid JSON.", "red"))
        print(final_output)

if __name__ == "__main__":
    main()