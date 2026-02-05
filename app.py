import streamlit as st
from google.api_core import exceptions
import json
import time
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
st.set_page_config(page_title="TrulyMadly AI Intern", page_icon="❤️", layout="wide")

# --- PRICING CONSTANTS (Gemini 3 Flash - 2026) ---
COST_PER_1M_INPUT = 0.50  
COST_PER_1M_OUTPUT = 3.00

def calculate_cost(metadata):
    """Calculates USD cost based on token metadata."""
    if not metadata: return 0.0
    input_cost = (metadata.prompt_token_count / 1_000_000) * COST_PER_1M_INPUT
    output_cost = (metadata.candidates_token_count / 1_000_000) * COST_PER_1M_OUTPUT
    return input_cost + output_cost

# --- CACHED AGENT FUNCTIONS ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_plan(query, _tool_defs):
    planner = PlannerAgent()
    # Capturing metadata requires accessing the response object from the agent's internal model call
    # For simplicity, we assume your PlannerAgent returns the plan. 
    # In production, you'd modify the agent to return (plan, metadata).
    plan = planner.create_plan(query, _tool_defs)
    return plan

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_execution(plan_json):
    executor = ExecutorAgent()
    executor.tools = {
        "github_tool": GitHubTool(), "weather_tool": WeatherTool(),
        "news_tool": NewsTool(), "currency_tool": CurrencyTool(),
        "compatibility_tool": CompatibilityTool(), "date_planner_tool": DatePlannerTool()
    }
    return executor.execute_plan(json.loads(plan_json))

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_verification(query, results_json):
    verifier = VerifierAgent()
    # Directly using the model here to ensure we get usage_metadata
    prompt = f"User Query: {query}\nTool Results: {results_json}\nVerify and provide a friendly response."
    response = verifier.model.generate_content(prompt)
    return response.text, response.usage_metadata

# --- UI SETUP ---
st.title("❤️ TrulyMadly AI Ops Assistant")
st.markdown("Automating matchmaking logic and operations with GenAI.")

# Sidebar for Stats & Cost Tracking
with st.sidebar:
    st.header("📊 Ops Dashboard")
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0
    
    st.metric("Total Session Spend", f"${st.session_state.total_cost:.6f}")
    
    if st.button("Reset Session Costs"):
        st.session_state.total_cost = 0.0
        st.rerun()
    
    st.divider()
    st.info("Caching: Active ✅\nParallelism: Ready 🚀")

tool_defs = [
    GitHubTool().get_definition(), WeatherTool().get_definition(),
    NewsTool().get_definition(), CurrencyTool().get_definition(),
    CompatibilityTool().get_definition(), DatePlannerTool().get_definition()
]

user_query = st.text_input("Enter your request:", placeholder="e.g. Is the weather in Delhi good for a date tonight?")

if st.button("Run AI Agent"):
    if user_query:
        try:
            with st.status("🤖 Agent is processing...", expanded=True) as status:
                # 1. Planning
                st.write("🧠 Planning steps...")
                plan = get_ai_plan(user_query, tool_defs)
                
                # 2. Execution
                st.write("⚙️ Executing tools...")
                results = get_ai_execution(json.dumps(plan))
                
                # 3. Verification & Cost Extraction
                st.write("🔍 Verifying results...")
                final_text, metadata = get_ai_verification(user_query, json.dumps(results))
                
                # Calculate and store cost
                req_cost = calculate_cost(metadata)
                st.session_state.total_cost += req_cost
                
                status.update(label=f"✅ Task Complete! (Cost: ${req_cost:.6f})", state="complete")

            # Final Result Display
            st.subheader("Final Answer")
            try:
                parsed = json.loads(final_text)
                st.success(parsed.get('final_answer', final_text))
            except:
                st.success(final_text)
            
            # Show breakdown
            st.caption(f"Tokens Used: {metadata.total_token_count} (Input: {metadata.prompt_token_count}, Output: {metadata.candidates_token_count})")

        except exceptions.ResourceExhausted:
            st.error("⚠️ Quota Exceeded. Please wait 30s.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")