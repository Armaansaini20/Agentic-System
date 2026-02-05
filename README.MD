# ❤️ TrulyMadly AI Ops Assistant

An intelligent, multi-agent orchestration system designed to automate matchmaking logic, date planning, and complex operational tasks. Built with **Google Gemini 3 Flash**, this assistant utilizes a robust "Planner-Executor-Verifier" architecture to handle multi-step user requests with high efficiency.

---

## 🚀 Features

* **Parallel Execution:** Leverages Python's `ThreadPoolExecutor` to trigger multiple tool calls simultaneously, significantly reducing latency.
* **Intelligent Planning:** A dedicated agent breaks down vague natural language into a structured, actionable execution JSON.
* **Operational Dashboard:** A custom Streamlit interface featuring real-time token tracking, session cost estimation, and agent health status.
* **TrulyMadly Specific Tools:** Custom-built engines for compatibility scoring and romantic date venue selection.
* **Dynamic Caching:** Integrated Streamlit caching to prevent redundant API calls and save on operational costs.

---

## 🏗️ Architecture Explanation

The system follows a **Modular Agent Swarm** pattern to ensure high accuracy and reliability:

1.  **Planner Agent (🧠):** The "Brain." It analyzes the user query against available tool definitions and creates a step-by-step plan. It marks independent tasks for parallel execution.
2.  **Executor Agent (⚙️):** The "Hands." It manages the technical execution of the plan, handling API authentication, error catching, and multi-threaded tool calls.
3.  **Verifier Agent (🔍):** The "Critic." It reviews raw technical data (JSON) from tools and synthesizes it into a brand-aligned, friendly, and "romantic" response for the end user.



---

## 🛠️ Setup Instructions

### 1. Prerequisites
* Python 3.10+
* Google AI Studio API Key (Gemini)
* TomTom or Google Maps API Key (for Date Planner)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/your-username/TrulyMadly-AIAgent.git](https://github.com/your-username/TrulyMadly-AIAgent.git)
cd TrulyMadly-AIAgent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Run the AppBashstreamlit run app.py
The application will be available locally at http://localhost:8501.🔑 Environment VariablesCreate a .env file in the root directory using the following template:Code snippet# .env
GEMINI_API_KEY=your_gemini_api_key_here
TOMTOM_API_KEY=your_tomtom_api_key_here
OPENWEATHER_API_KEY=your_weather_key_here
# Optional: Add GitHub or News API keys if applicable
🔌 Integrated APIs & ToolsToolSourcePurposeDate PlannerTomTom/GoogleFinds romantic venues in specific locations.CompatibilityCustom LogicCalculates "Match Scores" based on user interests.WeatherOpenWeatherChecks date suitability for outdoor activities.NewsGNews/NewsAPIProvides context for social media/ops updates.CurrencyExchangeRate-APIHelps with international marketing budget planning.💡 Example Prompts to TestThe Matchmaker: "I matched with someone who loves Sushi and Hiking in Bangalore. Suggest a compatibility score and 3 cafes for our first date."The Ops Manager: "What is the current weather in Mumbai, and is it a good day for an outdoor rooftop event?"The Multi-Tasker: "Convert 10,000 INR to USD and show me the latest tech news in India for our social media update."# ❤️ TrulyMadly AI Ops Assistant

An intelligent, multi-agent orchestration system designed to automate matchmaking logic, date planning, and complex operational tasks. Built with **Google Gemini 3 Flash**, this assistant utilizes a robust "Planner-Executor-Verifier" architecture to handle multi-step user requests with high efficiency.
```
---

## 🚀 Features

* **Parallel Execution:** Leverages Python's `ThreadPoolExecutor` to trigger multiple tool calls simultaneously, significantly reducing latency.
* **Intelligent Planning:** A dedicated agent breaks down vague natural language into a structured, actionable execution JSON.
* **Operational Dashboard:** A custom Streamlit interface featuring real-time token tracking, session cost estimation, and agent health status.
* **TrulyMadly Specific Tools:** Custom-built engines for compatibility scoring and romantic date venue selection.
* **Dynamic Caching:** Integrated Streamlit caching to prevent redundant API calls and save on operational costs.

---

## 🏗️ Architecture Explanation

The system follows a **Modular Agent Swarm** pattern to ensure high accuracy and reliability:

1.  **Planner Agent (🧠):** The "Brain." It analyzes the user query against available tool definitions and creates a step-by-step plan. It marks independent tasks for parallel execution.
2.  **Executor Agent (⚙️):** The "Hands." It manages the technical execution of the plan, handling API authentication, error catching, and multi-threaded tool calls.
3.  **Verifier Agent (🔍):** The "Critic." It reviews raw technical data (JSON) from tools and synthesizes it into a brand-aligned, friendly, and "romantic" response for the end user.

---

## Run the App 
```streamlit run app.py ```

The application will be available locally at http://localhost:8501.
🔑 Environment VariablesCreate a .env file in the root directory using the following template: Code snippet# .env
 .env - 
  ```GEMINI_API_KEY=''
  WEATHER_API_KEY=''
  NEWS_API_KEY=''
  EXCHANGE_RATE_KEY=''
  TOMTOM_API_KEY=''
  ```
---

## 🔌 Integrated APIs & Tools

| # | Tool | Source | Planner / Purpose |
| :--- | :--- | :--- | :--- |
| 1 | **Date Planner** | TomTom | Finds romantic venues in specific locations. |
| 2 | **Compatibility** | Custom Logic | Calculates "Match Scores" based on user interests. |
| 3 | **Weather** | OpenWeather | Checks date suitability for outdoor activities. |
| 4 | **News** | NewsAPI | Provides context for social media/ops updates. |
| 5 | **Currency** | ExchangeRate-API | Helps with international marketing budget planning. |
| 6 | **GitHub** | GitHub API | Manages repository tasks, creates issues, and summarizes PRs for dev ops. |

## Example Prompts to Test 
1. The Matchmaker: "I matched with someone who loves Sushi and Hiking in Bangalore. Suggest a compatibility score and 3 cafes for our first date.
2. "The Ops Manager: "What is the current weather in Mumbai, and is it a good day for an outdoor rooftop event?
3. "The Multi-Tasker: "Convert 10,000 INR to USD and show me the latest news in India for our social media update."

## ⚠️ Known Limitations & Tradeoffs API Quotas: 
1. The system is optimized for the Gemini Free Tier; however, intensive parallel queries may hit RPM (Requests Per Minute) limits.
2. Verification Hallucination: In rare cases, the Verifier might describe a venue's "vibe" based on training data rather than real-time reviews.
3. Stateless Conversations: The current version is optimized for single-turn complex tasks. Multi-turn chat memory is a roadmap item.




