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

# --- INITIALIZE SESSION STATE ---
# We need these to persist data across the st.rerun() call
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_query" not in st.session_state:
    st.session_state.last_query = None

# --- PRICING CONSTANTS ---
COST_PER_1M_INPUT = 0.50  
COST_PER_1M_OUTPUT = 3.00

def calculate_cost(metadata):
    if not metadata: return 0.0
    input_cost = (metadata.prompt_token_count / 1_000_000) * COST_PER_1M_INPUT
    output_cost = (metadata.candidates_token_count / 1_000_000) * COST_PER_1M_OUTPUT
    return input_cost + output_cost

# --- CACHED AGENT FUNCTIONS ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_plan(query, _tool_defs):
    planner = PlannerAgent()
    return planner.create_plan(query, _tool_defs)

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_execution(plan_json):
    executor = ExecutorAgent()
    return executor.execute_plan(json.loads(plan_json))

@st.cache_data(ttl=3600, show_spinner=False)
def get_ai_verification(query, results_json):
    verifier = VerifierAgent()
    return verifier.verify_and_respond(query, results_json)

# --- UI SETUP ---
st.title("❤️ TrulyMadly AI Ops Assistant")
st.markdown("Automating matchmaking logic and operations with GenAI.")

st.markdown("Would work for 5 queries due to rate limiting on Gemini Free Tier - For more testing input own Gemini Key")

# --- SIDEBAR: Ops Dashboard, Agents & Tools ---
with st.sidebar:
    st.header("📊 Ops Dashboard")
    
    # Metric updates instantly because of the st.rerun() in the loop below
    st.metric("Total Session Spend", f"${st.session_state.total_cost:.6f}")
    
    if st.button("Reset Session Costs"):
        st.session_state.total_cost = 0.0
        st.session_state.last_answer = None
        st.rerun()
    
    st.divider()
    
    st.subheader("🤖 Connected Agents")
    st.success("🧠 Planner Agent: ONLINE")
    st.success("⚙️ Executor Agent: ONLINE")
    st.success("🔍 Verifier Agent: ONLINE")
    
    st.divider()
    
    st.subheader("🛠️ Operational Tools")
    st.info("📂 GitHub Operations")
    st.info("☁️ Weather Insights")
    st.info("📰 Global News")
    st.info("💱 Currency Exchange")
    st.info("🤝 Compatibility Engine")
    st.info("📍 Date Venue Planner")
    
    st.divider()
    st.caption("Caching: Active ✅ | Parallelism: Multi-threaded 🚀")

# --- SAMPLE QUERIES SECTION ---
st.subheader("💡 Sample Queries")
samples = {
    "Select a sample query...": "",
    "Compatibility Check (Planner + Compatibility Tool)": "I matched with someone who loves Sushi and Hiking. We are in Bangalore. Suggest a compatibility score.",
    "Date Planning (Planner + Date Tool)": "Find 3 romantic cafes in Bellandur, Bangalore.",
    "Weather + News (Parallel Execution: Multi-Agent)": "What is the weather in Delhi and show me the latest tech news in India.",
    "Currency Budget (Planner + Currency Tool)": "Convert 10,000 INR to USD for our marketing campaign."
}

selected_sample = st.selectbox("Choose a test case:", list(samples.keys()))
query_value = samples[selected_sample] if selected_sample != "Select a sample query..." else ""
user_query = st.text_input("📝 Enter your request:", value=query_value, placeholder="e.g. Suggest 3 cafes in Mumbai.")

tool_defs = [
    GitHubTool().get_definition(), WeatherTool().get_definition(),
    NewsTool().get_definition(), CurrencyTool().get_definition(),
    CompatibilityTool().get_definition(), DatePlannerTool().get_definition()
]

# --- MAIN AGENT LOOP ---
if st.button("Run AI Agent"):
    if user_query:
        try:
            with st.status("🤖 Agent Swarm Processing...", expanded=True) as status:
                # 1. Planning
                st.write("🧠 **Planner Agent** is breaking down the request...")
                plan, plan_metadata = get_ai_plan(user_query, tool_defs)
                plan_cost = calculate_cost(plan_metadata)
                
                # 2. Execution
                st.write("⚙️ **Executor Agent** is firing tools in parallel...")
                results = get_ai_execution(json.dumps(plan))
                
                # 3. Verification
                st.write("🔍 **Verifier Agent** is synthesizing the final response...")
                final_output = get_ai_verification(user_query, json.dumps(results))
                
                status.update(label=f"✅ Task Complete!", state="complete")

            # Update Session State before rerun
            st.session_state.total_cost += plan_cost
            st.session_state.last_query = user_query
            
            if isinstance(final_output, dict):
                st.session_state.last_answer = final_output.get('final_answer', "No response generated.")
            else:
                st.session_state.last_answer = final_output
            
            # This triggers the sidebar cost to update immediately
            st.rerun()

        except exceptions.ResourceExhausted:
            st.error("⚠️ Quota Exceeded. Please wait 30 seconds.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- PERSISTENT DISPLAY (Outside the button block) ---
if st.session_state.last_answer:
    st.divider()
    st.subheader("💌 Final Answer")
    st.success(st.session_state.last_answer)
    st.caption(f"Query processed by: **Planner**, **Executor**, and **Verifier** agents.")
    
    # Optional: Show detailed breakdown in an expander that stays visible
    with st.expander("🔍 System Trace & Insights"):
        st.write(f"**Last Query:** {st.session_state.last_query}")
        st.write(f"**Session Economics:** Cumulative Spend is ${st.session_state.total_cost:.6f}")