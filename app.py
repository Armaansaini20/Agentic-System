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
st.set_page_config(page_title="TrulyMadly AI Intern", page_icon="❤️")

# --- CACHED AGENT FUNCTIONS ---
# We use ttl (Time To Live) so the cache clears periodically
@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_plan(query, _tool_defs):
    planner = PlannerAgent()
    return planner.create_plan(query, _tool_defs)

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_execution(plan_json):
    executor = ExecutorAgent()
    executor.tools = {
        "github_tool": GitHubTool(), "weather_tool": WeatherTool(),
        "news_tool": NewsTool(), "currency_tool": CurrencyTool(),
        "compatibility_tool": CompatibilityTool(), "date_planner_tool": DatePlannerTool()
    }
    # Note: For parallel execution, ensure your executor.py uses ThreadPoolExecutor
    return executor.execute_plan(json.loads(plan_json))

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_verification(query, results_json):
    verifier = VerifierAgent()
    # We return the raw response object to extract token metadata
    response = verifier.model.generate_content(f"Verify: {query} with data {results_json}")
    return response.text, response.usage_metadata

# --- UI SETUP ---
st.title("❤️ TrulyMadly AI Ops Assistant")
st.markdown("Automating matchmaking logic and operations with GenAI.")

# Sidebar for Stats
with st.sidebar:
    st.header("Ops Dashboard")
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0
    st.metric("Session Cost (Est.)", f"${st.session_state.total_cost:.6f}")
    st.info("Caching: Enabled ✅")

tool_defs = [
    GitHubTool().get_definition(), WeatherTool().get_definition(),
    NewsTool().get_definition(), CurrencyTool().get_definition(),
    CompatibilityTool().get_definition(), DatePlannerTool().get_definition()
]

user_query = st.text_input("Enter your request:", placeholder="e.g. Find 3 romantic cafes in Bangalore.")

if st.button("Run AI Agent"):
    if user_query:
        try:
            with st.status("🤖 Agent is processing...", expanded=True) as status:
                st.write("🧠 Thinking (Planning)...")
                plan = get_ai_plan(user_query, tool_defs)
                
                st.write("⚙️ Running Tools (Parallel)...")
                results = get_ai_execution(json.dumps(plan))
                
                st.write("🔍 Verifying & Formatting...")
                final_text, metadata = get_ai_verification(user_query, json.dumps(results))
                
                # Cost Calculation (Gemini 1.5 Flash Pricing)
                cost = (metadata.prompt_token_count * 0.000000075) + (metadata.candidates_token_count * 0.0000003)
                st.session_state.total_cost += cost
                
                status.update(label=f"✅ Done (Cost: ${cost:.6f})", state="complete")

            st.subheader("Final Answer")
            try:
                # Assuming Verifier returns JSON-like string
                parsed = json.loads(final_text)
                st.info(parsed.get('final_answer', final_text))
            except:
                st.info(final_text)

        except exceptions.ResourceExhausted:
            st.error("⚠️ Quota Exceeded. Please wait 30s.")
        except Exception as e:
            st.error(f"Error: {e}")