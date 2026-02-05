import streamlit as st
import json
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool
from tools.currency_tool import CurrencyTool
from tools.compatibility_tool import CompatibilityTool
from tools.date_planner_tool import DatePlannerTool

# UI Configuration
st.set_page_config(page_title="TrulyMadly AI Intern", page_icon="❤️")

st.title("❤️ TrulyMadly AI Ops Assistant")
st.markdown("Automating matchmaking logic and operations with GenAI.")

# Sidebar for Tool Status
with st.sidebar:
    st.header("Tool Status")
    st.success("GitHub & Weather: Connected")
    st.success("NewsTool and CurrencyExchange: Cinnected")
    st.success("Compatibility Agent: Online")
    st.success("TomTom Maps: Active")

# Initialize Agents
planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()

# Dynamic Tool Registry
tool_defs = [
    GitHubTool().get_definition(), 
    WeatherTool().get_definition(),
    NewsTool().get_definition(),
    CurrencyTool().get_definition(),
    CompatibilityTool().get_definition(),
    DatePlannerTool().get_definition()
]

# User Input
user_query = st.text_input("Enter your request:", placeholder="e.g. Find 3 romantic cafes in Bellandur for a match who loves sushi.")

if st.button("Run AI Agent"):
    if user_query:
        with st.status("🤖 Agent is working...", expanded=True) as status:
            # 1. Planning
            st.write("🧠 Planning steps...")
            plan = planner.create_plan(user_query, tool_defs)
            
            # 2. Execution
            st.write("⚙️ Executing tools...")
            # Ensure executor has tools mapped
            executor.tools = {
                "github_tool": GitHubTool(), "weather_tool": WeatherTool(),
                "news_tool": NewsTool(), "currency_tool": CurrencyTool(),
                "compatibility_tool": CompatibilityTool(), "date_planner_tool": DatePlannerTool()
            }
            results = executor.execute_plan(plan)
            
            # 3. Verification
            st.write("🔍 Verifying results...")
            final_output = verifier.verify_and_respond(user_query, results)
            status.update(label="✅ Task Complete!", state="complete", expanded=False)

        # Final Result Display
        try:
            parsed = json.loads(final_output)
            st.subheader("Final Answer")
            st.info(parsed.get('final_answer', "Error generating response."))
            
            with st.expander("View Internal Reasoning (Raw Data)"):
                st.json(results)
        except:
            st.error("Could not parse final answer.")
    else:
        st.warning("Please enter a query.")